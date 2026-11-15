"""LLM Router Pattern — runnable demo.

Classifies queries by complexity (rules-based) and routes them to a tier
(small/medium/large). CascadeRouter adds quality-gated escalation: low
confidence or thin responses re-route one tier up.

No external dependencies — generate is mocked so the demo runs offline.
Swap `mock_generate` for real provider calls to use it for real.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import re


@dataclass
class ModelConfig:
    name: str
    max_tokens: int
    cost_per_1k: float   # USD per 1K output tokens (illustrative)
    latency_ms: int


@dataclass
class Response:
    model: str
    content: str
    tokens_used: int
    cost: float


MODELS = {
    "small":  ModelConfig("gpt-4o-mini",  4096, 0.0006, 200),
    "medium": ModelConfig("gpt-4o",       8192, 0.005,  500),
    "large":  ModelConfig("o1",          16384, 0.015,  2000),
}


def classify_complexity(text: str) -> Tuple[str, float]:
    """Classify query complexity; return (level, confidence 0-1)."""
    lower = text.lower()
    word_count = len(text.split())
    score = 0

    complex_patterns = [
        r"analyze|design|architect|compare|evaluate",
        r"debug|refactor|optimize|review",
        r"step.by.step|detailed|thorough",
        r"legal|medical|financial|security",
    ]
    simple_patterns = [
        r"^\s*(what|who|when|where|is|are|can|do)\s",
        r"calculate|convert|format|translate",
        r"summarize|rewrite|paraphrase",
    ]

    for pattern in complex_patterns:
        if re.search(pattern, lower):
            score += 2
    for pattern in simple_patterns:
        if re.search(pattern, lower):
            score -= 2

    if word_count > 100:
        score += 2
    elif word_count < 20:
        score -= 1

    if score >= 2:
        return "high", min(0.5 + score * 0.15, 1.0)
    if score <= -2:
        return "low", min(0.5 - score * 0.15, 1.0)
    return "medium", 0.5  # the gray zone: no strong signal either way


def route_to_model(complexity: str) -> str:
    return {"low": "small", "medium": "medium", "high": "large"}.get(complexity, "medium")


TIER_RANK = {"small": 0, "medium": 1, "large": 2}
LEVEL_RANK = {"low": 0, "medium": 1, "high": 2}


def mock_generate(tier: str, model: ModelConfig, prompt: str) -> Response:
    """Mock generation — a tier under the query's true level answers thin."""
    required = LEVEL_RANK[classify_complexity(prompt)[0]]
    if TIER_RANK[tier] < required:
        return Response(model.name, f"[{model.name}] I can't fully answer that.", 12, 0.0)
    tokens = min(max(60, len(prompt.split()) * 2), model.max_tokens)
    cost = (tokens / 1000) * model.cost_per_1k
    return Response(model.name, f"[{model.name}] Response to: {prompt[:50]}...", tokens, cost)


class LLMRouter:
    """One-shot router: classify once, send to the mapped tier."""

    def __init__(self, models: Dict[str, ModelConfig]):
        self.models = models
        self.stats = {"routed": 0, "escalated": 0, "total_cost": 0.0, "baseline_cost": 0.0}

    def _charge(self, response: Response) -> Response:
        self.stats["routed"] += 1
        self.stats["total_cost"] += response.cost
        self.stats["baseline_cost"] += (response.tokens_used / 1000) * self.models["large"].cost_per_1k
        return response

    def handle(self, query_text: str) -> Response:
        complexity, confidence = classify_complexity(query_text)
        model_key = route_to_model(complexity)
        print(f"  [{complexity} @ {confidence:.2f}] -> {self.models[model_key].name}")
        return self._charge(mock_generate(model_key, self.models[model_key], query_text))


class CascadeRouter(LLMRouter):
    """Start cheap, verify the response, escalate one tier on failure."""

    TIERS = ["small", "medium", "large"]

    def _quality_ok(self, response: Response) -> bool:
        return response.tokens_used >= 30 and "I can't" not in response.content

    def handle(self, query_text: str) -> Response:
        complexity, confidence = classify_complexity(query_text)
        start = self.TIERS.index(route_to_model(complexity))
        if confidence < 0.7:
            start = max(start - 1, 0)  # unsure: start one tier lower, verify

        for tier in self.TIERS[start:]:
            response = mock_generate(tier, self.models[tier], query_text)
            self._charge(response)
            if self._quality_ok(response) or tier == "large":
                print(f"  [{complexity} @ {confidence:.2f}] -> {self.models[tier].name}")
                return response
            self.stats["escalated"] += 1
            print(f"  [{complexity} @ {confidence:.2f}] {self.models[tier].name} thin -> escalate")
        return response


QUERIES = [
    "What is the capital of France?",
    "Analyze this contract for liability clauses and suggest revisions",
    "Convert 100 degrees Celsius to Fahrenheit",
    "Design a microservices architecture for an e-commerce platform with 10M users",
    "Translate 'good morning' to Spanish",
    "Should I refactor this function or leave it as is?",  # borderline -> medium
]


def _report(router: LLMRouter) -> None:
    savings = 1 - router.stats["total_cost"] / max(router.stats["baseline_cost"], 1e-9)
    print(f"  {router.stats['routed']} calls | {router.stats['escalated']} escalations"
          f" | cost ${router.stats['total_cost']:.6f} vs always-large"
          f" ${router.stats['baseline_cost']:.6f} | saved {savings:.0%}")


if __name__ == "__main__":
    print("== One-shot router ==")
    router = LLMRouter(MODELS)
    for q in QUERIES:
        router.handle(q)
    _report(router)

    print("\n== Cascade router (verify + escalate) ==")
    cascade = CascadeRouter(MODELS)
    for q in QUERIES:
        cascade.handle(q)
    _report(cascade)
