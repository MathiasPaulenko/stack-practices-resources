# pytest-cov Sample Project

Companion project for the StackPractices recipe [Measure and Enforce Python Test Coverage with pytest-cov](https://stackpractices.com/recipes/python-coverage-pytest-cov/).

## Files

- `pyproject.toml` — coverage configuration with `[tool.coverage.*]`.
- `.coveragerc` — legacy `coverage.py` config file.
- `tox.ini` — run tests across Python versions with `pytest-cov`.
- `github_actions_coverage.yml` — GitHub Actions workflow with Codecov and `diff-cover`.
- `sample_app/` — tiny package with `User` and `UserService`.
- `tests/` — pytest test suite.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -e ".[test]"
pytest
```

This runs the tests and enforces `fail_under = 80` with branch coverage.

## Useful commands

```bash
pytest --cov=sample_app --cov-report=html
pytest -n auto --cov=sample_app --cov-report=term-missing
coverage combine
coverage report
diff-cover coverage.xml --compare-branch=origin/main --fail-under=100
```
