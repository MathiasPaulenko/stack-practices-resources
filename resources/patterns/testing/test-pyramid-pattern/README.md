# Test Pyramid — Companion Resources

Companion code for the [Test Pyramid pattern](https://stackpractices.com/patterns/test-pyramid-pattern/) on StackPractices.

## Files

| File | Language | Description |
| --- | --- | --- |
| `pricing.js` | JavaScript (ESM) | Pricing domain logic exercised by the unit tests |
| `calculator.test.js` | JavaScript + Vitest | Unit layer example: fast, isolated, deterministic tests |
| `pricing.py` | Python 3.10+ | Same pricing logic in Python |
| `test_pricing.py` | Python + pytest | Unit layer example for the Python implementation |
| `checkout.e2e.spec.ts` | TypeScript + Playwright | E2E layer example: a critical checkout journey |
| `report_test_distribution.py` | Python 3.10+ | Counts tests per layer and warns when E2E share exceeds 15% |
| `smoke-test.sh` | Bash + curl + jq | Minimal post-deploy smoke check |
| `test-pyramid-ci.yml` | GitHub Actions | Layered pipeline: unit → integration → E2E |

## Quick start

### JavaScript unit tests (Vitest)

```bash
npm install -D vitest
npx vitest run calculator.test.js
# Output: 5 passed
```

### Python unit tests (pytest)

```bash
python -m pytest test_pricing.py -v
# Output: 4 passed
```

### Measure a suite's pyramid distribution

```bash
python report_test_distribution.py
# Unit:        312 (68%)
# Integration:  104 (23%)
# E2E:           41 (9%)
```

### Smoke test after a deploy

```bash
BASE_URL=https://api.example.com ./smoke-test.sh
```

### Layered CI pipeline

Copy `test-pyramid-ci.yml` to `.github/workflows/tests.yml`. Each layer runs only if the cheaper layer below it passed, keeping feedback fast and CI minutes low.
