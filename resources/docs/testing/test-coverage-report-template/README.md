# Test Coverage Report Template — Companion

Companion files for the [Test Coverage Report Template](https://stackpractices.com/docs/test-coverage-report-template/).

## Files

| File | What it is |
|------|-----------|
| `aggregate-coverage.mjs` | Node script that turns a c8/istanbul `coverage-summary.json` into the per-module markdown table used by the template |
| `coverage-summary-sample.json` | Sample c8 output to test the script against |
| `example-report.md` | A filled-in report showing the finished result |

## Usage

```bash
# 1. generate coverage with your runner
npx vitest run --coverage --reporter=json-summary

# 2. aggregate per module (default root: src/modules/, override with an arg)
node aggregate-coverage.mjs coverage/coverage-summary.json src/modules/
```

Try it against the sample data:

```bash
node aggregate-coverage.mjs coverage-summary-sample.json src/modules/
```

Paste the output into section 2 of the report. The script averages per-file coverage per module directory — adapt `moduleRoot` to your layout (`packages/`, `services/` for monorepos).
