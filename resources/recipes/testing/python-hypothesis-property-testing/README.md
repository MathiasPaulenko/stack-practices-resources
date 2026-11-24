# Property-Based Testing with Hypothesis — Companion Files

Runnable test suite for the recipe
[Property-Based Testing with Hypothesis](https://stackpractices.com/recipes/python-hypothesis-property-testing/).

## Files

- `test_properties.py` — core property tests: string/list/dict strategies, JSON round-trip, `assume`, `@example`, `@settings`.
- `test_strategies.py` — a `@composite` email generator and `st.builds` over a dataclass.
- `test_stateful.py` — `RuleBasedStateMachine` modeling a stack with push/pop rules and a size invariant.
- `requirements.txt` — `hypothesis`, `pytest`.

## Usage

```bash
pip install -r requirements.txt
pytest -v
```

Deliberately break a property (e.g., change `test_min_le_max` to `min(lst) < max(lst)`) and watch Hypothesis shrink the counterexample to a single-element list.
