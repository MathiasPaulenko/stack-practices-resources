# Software Testing Strategy Guide — Companion

Runnable pieces that implement the layered testing strategy described in the guide:

- `ci-test-workflow.yml` — GitHub Actions workflow with the pyramid stages (unit → integration → E2E) and a coverage regression gate on pull requests.
- `unit_tests_pytest.py` — parametrized unit test example (pytest). Run it with `pytest unit_tests_pytest.py -v`.

## Usage

1. Copy `ci-test-workflow.yml` to `.github/workflows/test.yml` in your repo.
2. Adapt the `npm run test:*` commands to your project's test scripts.
3. Keep the layer order: fast unit tests first, expensive E2E last — that order is what keeps feedback under ~10 minutes.

Source article: <https://stackpractices.com/guides/testing-strategy-guide/>
