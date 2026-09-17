"""Event-driven Blackboard variant: sources react to blackboard changes.

Unlike blackboard-solver.py (controller polls sources), here the blackboard
notifies subscribers on every change and sources fire themselves.

    python blackboard-event-driven.py "cancel my subscription"

Standard library only.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Callable


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
    _subscribers: list[Callable[["Blackboard"], None]] = field(default_factory=list)

    def subscribe(self, listener: Callable[["Blackboard"], None]) -> None:
        self._subscribers.append(listener)

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        self.hypotheses.append(hypothesis)
        # notify every subscriber — a source may want to react to this new fact
        for listener in self._subscribers:
            listener(self)


class KeywordMatcher:
    name = "KeywordMatcher"
    KEYWORDS = {
        "billing": ("invoice", "charge", "refund", "payment"),
        "account": ("password", "login", "email", "profile"),
        "cancellation": ("cancel", "unsubscribe", "subscription"),
    }

    def on_change(self, bb: Blackboard) -> None:
        if any(h.source == self.name for h in bb.hypotheses) or bb.complete:
            return
        text = bb.text.lower()
        for intent, words in self.KEYWORDS.items():
            if any(w in text for w in words):
                bb.add_hypothesis(Hypothesis(f"intent={intent}", Confidence.LOW, self.name))


class SentimentAnalyzer:
    name = "SentimentAnalyzer"
    NEGATIVE = {"cancel", "broken", "angry", "refund", "hate", "frustrated"}

    def on_change(self, bb: Blackboard) -> None:
        if any(h.source == self.name for h in bb.hypotheses) or bb.complete:
            return
        if not any(h.source == "KeywordMatcher" for h in bb.hypotheses):
            return
        words = set(bb.text.lower().split())
        sentiment = "negative" if words & self.NEGATIVE else "neutral"
        bb.add_hypothesis(Hypothesis(f"sentiment={sentiment}", Confidence.MEDIUM, self.name))


class ConfidenceEvaluator:
    name = "ConfidenceEvaluator"

    def on_change(self, bb: Blackboard) -> None:
        if bb.complete:
            return
        intent = next((h for h in bb.hypotheses if "intent=" in h.content), None)
        sentiment = next((h for h in bb.hypotheses if "sentiment=" in h.content), None)
        if intent and sentiment:
            solution = f"{intent.content} ({sentiment.content})"
            bb.final_solution = solution
            bb.complete = True
            bb.hypotheses.append(Hypothesis(solution, Confidence.HIGH, self.name))


def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else "cancel my subscription"
    bb = Blackboard(text=text)

    # sources subscribe themselves; there is no controller loop
    for src in (KeywordMatcher(), SentimentAnalyzer(), ConfidenceEvaluator()):
        bb.subscribe(src.on_change)

    # kick off: seed the board so subscribers start reacting
    bb.add_hypothesis(Hypothesis("analysis started", Confidence.LOW, "seed"))

    for h in bb.hypotheses:
        print(f"[{h.confidence.name:6}] {h.source:20} -> {h.content}")
    print(f"Solution: {bb.final_solution or 'none'}")


if __name__ == "__main__":
    main()
