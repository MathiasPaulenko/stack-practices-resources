"""Blackboard pattern: runnable text-classification demo.

Three knowledge sources cooperate on a shared blackboard to classify a
text snippet. Run it:

    python blackboard-solver.py "cancel my subscription"

No dependencies — standard library only.
"""
from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum


class Confidence(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Hypothesis:
    content: str
    confidence: Confidence
    source: str


@dataclass
class Blackboard:
    text: str
    hypotheses: list[Hypothesis] = field(default_factory=list)
    final_solution: str | None = None
    complete: bool = False

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        self.hypotheses.append(hypothesis)

    def best_hypothesis(self) -> Hypothesis | None:
        if not self.hypotheses:
            return None
        return max(self.hypotheses, key=lambda h: h.confidence)


class KnowledgeSource(ABC):
    """Each source inspects the blackboard and may add hypotheses."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def can_contribute(self, blackboard: Blackboard) -> bool: ...

    @abstractmethod
    def contribute(self, blackboard: Blackboard) -> None: ...


class KeywordMatcher(KnowledgeSource):
    """Weak signal: keyword hits only produce LOW hypotheses."""

    KEYWORDS = {
        "billing": ("invoice", "charge", "refund", "payment"),
        "account": ("password", "login", "email", "profile"),
        "cancellation": ("cancel", "unsubscribe", "subscription"),
    }

    def can_contribute(self, blackboard: Blackboard) -> bool:
        return not any(h.source == self.name for h in blackboard.hypotheses)

    def contribute(self, blackboard: Blackboard) -> None:
        text = blackboard.text.lower()
        for intent, words in self.KEYWORDS.items():
            if any(w in text for w in words):
                blackboard.add_hypothesis(
                    Hypothesis(f"intent={intent}", Confidence.LOW, self.name)
                )


class SentimentAnalyzer(KnowledgeSource):
    """Medium signal: sentiment narrows the hypothesis space."""

    NEGATIVE = {"cancel", "broken", "angry", "refund", "hate", "frustrated"}

    def can_contribute(self, blackboard: Blackboard) -> bool:
        already_ran = any(h.source == self.name for h in blackboard.hypotheses)
        return not already_ran and any(
            h.source == "KeywordMatcher" for h in blackboard.hypotheses
        )

    def contribute(self, blackboard: Blackboard) -> None:
        words = set(blackboard.text.lower().split())
        sentiment = "negative" if words & self.NEGATIVE else "neutral"
        blackboard.add_hypothesis(
            Hypothesis(f"sentiment={sentiment}", Confidence.MEDIUM, self.name)
        )


class ConfidenceEvaluator(KnowledgeSource):
    """Closes the loop once a LOW hypothesis exists plus any MEDIUM support."""

    def can_contribute(self, blackboard: Blackboard) -> bool:
        has_intent = any("intent=" in h.content for h in blackboard.hypotheses)
        has_sentiment = any(h.confidence == Confidence.MEDIUM for h in blackboard.hypotheses)
        return has_intent and has_sentiment

    def contribute(self, blackboard: Blackboard) -> None:
        intent = next(h for h in blackboard.hypotheses if "intent=" in h.content)
        sentiment = next(h for h in blackboard.hypotheses if "sentiment=" in h.content)
        blackboard.add_hypothesis(
            Hypothesis(
                f"{intent.content} ({sentiment.content})",
                Confidence.HIGH,
                self.name,
            )
        )
        blackboard.final_solution = f"{intent.content} ({sentiment.content})"
        blackboard.complete = True


class Controller:
    """Picks the first eligible source each round until done or limit hit."""

    def __init__(self, blackboard: Blackboard, sources: list[KnowledgeSource], max_iterations: int = 20):
        self.blackboard = blackboard
        self.sources = sources
        self.max_iterations = max_iterations

    def solve(self) -> None:
        for _ in range(self.max_iterations):
            if self.blackboard.complete:
                return
            for source in self.sources:
                if source.can_contribute(self.blackboard):
                    source.contribute(self.blackboard)
                    break


def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else "cancel my subscription"
    blackboard = Blackboard(text=text)
    controller = Controller(
        blackboard,
        [KeywordMatcher("KeywordMatcher"), SentimentAnalyzer("SentimentAnalyzer"), ConfidenceEvaluator("ConfidenceEvaluator")],
    )
    controller.solve()
    for h in blackboard.hypotheses:
        print(f"[{h.confidence.name:6}] {h.source:20} -> {h.content}")
    print(f"Solution: {blackboard.final_solution or 'none'}")


if __name__ == "__main__":
    main()
