"""A/B testing harness for prompt versions.

Routes traffic between two prompt versions, records correctness,
and reports the winner with per-variant accuracy.
"""
import json
import random
from collections import defaultdict


class PromptABTest:
    def __init__(self, prompt_a: str, prompt_b: str, traffic_split: float = 0.5):
        self.prompt_a = prompt_a
        self.prompt_b = prompt_b
        self.traffic_split = traffic_split
        self.results = defaultdict(lambda: {"correct": 0, "total": 0})

    def route(self) -> tuple[str, str]:
        if random.random() < self.traffic_split:
            return self.prompt_a, "A"
        return self.prompt_b, "B"

    def record(self, variant: str, correct: bool) -> None:
        self.results[variant]["total"] += 1
        if correct:
            self.results[variant]["correct"] += 1

    def report(self) -> dict:
        a = self.results["A"]
        b = self.results["B"]

        return {
            "variant_a": {
                "accuracy": a["correct"] / a["total"] if a["total"] > 0 else 0,
                "samples": a["total"],
            },
            "variant_b": {
                "accuracy": b["correct"] / b["total"] if b["total"] > 0 else 0,
                "samples": b["total"],
            },
            "winner": "A"
            if a["correct"] / max(a["total"], 1) > b["correct"] / max(b["total"], 1)
            else "B",
        }


if __name__ == "__main__":
    ab_test = PromptABTest(
        prompt_a="prompts/classifier/versions/3.1.0.md",
        prompt_b="prompts/classifier/versions/3.2.0.md",
    )
    # Simulate 1000 samples
    for _ in range(1000):
        _, variant = ab_test.route()
        ab_test.record(variant, correct=random.random() > 0.1)
    print(json.dumps(ab_test.report(), indent=2))
