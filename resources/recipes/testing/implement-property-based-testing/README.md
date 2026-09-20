# Implement Property-Based Testing

Companion project for the StackPractices recipe [Implement Property-Based Testing](https://stackpractices.com/recipes/implement-property-based-testing/).

## Files

- `python/test_property_based.py` — Hypothesis properties: involution, constrained strategies, a composite `users` strategy, a JSON round-trip and a `RuleBasedStateMachine` stack.
- `javascript/property-based.mjs` — fast-check properties and a model-based test driven by `fc.commands` with `Command` objects (`check`/`run`).
- `java/` — Maven project with jqwik properties and an `ActionChain` stateful test over `Stack<Integer>`.

## Quick start

```bash
# Python (Hypothesis)
cd python && pip install -r requirements.txt && pytest test_property_based.py -v

# JavaScript (fast-check)
cd javascript && npm install && npm test

# Java (jqwik)
cd java && mvn test
```

All examples pass as written. To see shrinking in action, change `reverse` in the Python file to a broken implementation (e.g., `return s`) and rerun — Hypothesis reports the minimal counterexample plus a reproducible seed.
