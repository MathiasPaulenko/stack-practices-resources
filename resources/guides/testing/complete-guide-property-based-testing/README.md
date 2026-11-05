# Property-Based Testing Examples

Companion resources for [Property-Based Testing Guide](https://stackpractices.com/guides/complete-guide-property-based-testing/).

## Contents

| File | Purpose |
| --- | --- |
| `test_string_properties.py` | Basic Hypothesis properties (roundtrip, invariants) |
| `test_user_properties.py` | Composite strategies, `@example`, JSON roundtrip |
| `test_stack_stateful.py` | `RuleBasedStateMachine` stateful testing |
| `conftest.py` | Hypothesis dev/ci profiles (`HYPOTHESIS_PROFILE`) |
| `properties.test.ts` | fast-check suite: strings, users, stateful stack |
| `package.json` | Dependencies for the TypeScript suite |
| `property-t
