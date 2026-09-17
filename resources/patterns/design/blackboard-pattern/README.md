# Blackboard Pattern — Companion Resources

Companion code for the StackPractices resource
[Blackboard Pattern](https://stackpractices.com/patterns/blackboard-pattern/).

## Contents

- `blackboard-solver.py` — runnable text-classification demo: three knowledge sources
  (keyword matcher, sentiment analyzer, confidence evaluator) cooperate on a shared
  blackboard until a solution converges. Standard library only.
- `blackboard-event-driven.py` — the event-driven variant: sources subscribe to
  blackboard changes and fire themselves; no controller loop.

## Usage

```bash
python blackboard-solver.py "cancel my subscription"
python blackboard-event-driven.py "cancel my subscription"
```

Output shows each hypothesis as it's contributed, with confidence and source:

```text
[LOW   ] KeywordMatcher       -> intent=cancellation
[MEDIUM] SentimentAnalyzer    -> sentiment=negative
[HIGH  ] ConfidenceEvaluator  -> intent=cancellation (sentiment=negative)
Solution: intent=cancellation (sentiment=negative)
```

## Ideas to extend

- Add a fourth knowledge source (e.g., entity extraction) and watch the controller pick it up.
- Swap the linear `Controller` for a priority queue where each source bids on relevance.
- Add iteration logging to trace why the solution converged — or didn't.
