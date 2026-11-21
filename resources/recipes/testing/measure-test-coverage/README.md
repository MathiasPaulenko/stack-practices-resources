# Measure Test Coverage — Companion Resources

Runnable coverage configurations for the [Measure Test Coverage](https://stackpractices.com/recipes/measure-test-coverage/) recipe on StackPractices.

| File | What it is |
|------|------------|
| `pyproject-coverage.toml` | coverage.py / pytest-cov config: branch coverage, omit rules, `fail_under = 80`, practical `exclude_also` entries |
| `vitest.config.ts` | Vitest coverage with the correct `coverage.thresholds` shape (Vitest 1.x+) and `lcov` reporter for trend tools |
| `jacoco-pom-snippet.xml` | JaCoCo Maven plugin: report on `test`, `check` goal with BUNDLE rules plus a stricter PACKAGE rule for core code |
| `coverage-gate.yml` | GitHub Actions pipeline: parallel test groups emit partial coverage, a merge job combines them and enforces the gate |

## Notes

- `--cov` takes the importable package name, not the tests directory — that's the most common cause of 0% reports.
- Always emit an XML or lcov report alongside HTML: humans read HTML, tools read XML.
- Gate on diffs and trends, not a magic number. Ratchet thresholds up as the suite improves.
