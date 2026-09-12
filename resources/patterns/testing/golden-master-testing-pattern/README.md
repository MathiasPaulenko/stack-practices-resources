# Golden Master Testing — Companion Resources

Companion code for the [Golden Master Testing Pattern](https://stackpractices.com/patterns/golden-master-testing-pattern/) on StackPractices.

## Files

| File | Language | Description |
| --- | --- | --- |
| `legacy_calculator.py` | Python 3.12+ | The legacy system we want to refactor (no tests, unclear behavior) |
| `refactored_calculator.py` | Python 3.12+ | The refactored version using a dispatch table |
| `generate_golden_master.py` | Python 3.12+ | Generates 258 test inputs, runs legacy system, saves golden master |
| `test_golden_master.py` | Python 3.12+ + pytest 8.3 | Verifies refactored code matches golden master (258 parametrized cases) |
| `test_inputs.json` | JSON | 3 sample test inputs for quick testing |
| `golden_master.json` | JSON | 258 captured outputs with SHA-256 hashes |
| `normalize_output.py` | Python 3.12+ | Normalizes non-deterministic values (timestamps, UUIDs, IDs) |

## Quick start

### Generate the golden master (before refactoring)

```bash
python generate_golden_master.py golden_master.json
# Output: Golden master generated with 258 cases -> golden_master.json
```

### Run golden master tests (after refactoring)

```bash
python -m pytest test_golden_master.py -v
# Output: 258 passed
```

### Verify a single input

```bash
echo '{"operation":"add","a":1,"b":2}' | python legacy_calculator.py
echo '{"operation":"add","a":1,"b":2}' | python refactored_calculator.py
# Both should produce identical output
```

## How it works

1. `generate_golden_master.py` creates 258 diverse inputs (normal, edge, boundary cases) and runs them through `legacy_calculator.py`.
2. For each input, it captures the output and computes a SHA-256 hash.
3. All inputs, outputs, and hashes are saved to `golden_master.json`.
4. `test_golden_master.py` runs the same inputs through `refactored_calculator.py` and compares hashes.
5. If all 258 hashes match, the refactoring preserved behavior.

## Workflow

```bash
# Step 1: Generate golden master (before any changes)
python generate_golden_master.py

# Step 2: Refactor legacy_calculator.py -> refactored_calculator.py

# Step 3: Run golden master tests
python -m pytest test_golden_master.py -v

# Step 4: If all pass, refactoring is safe. Delete golden master when you have proper unit tests.
```
