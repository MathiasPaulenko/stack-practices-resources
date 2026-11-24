# Pytest Fixtures and Parametrize — Companion Resources

Companion files for [Pytest Fixtures and Parametrize](https://stackpractices.com/recipes/python-pytest-fixtures-parametrize/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `conftest.py` | Shared fixtures: session-scope env setup, indirect-param fixture via `request.param`, parametrized fixture with `params`, autouse cleanup |
| `test_parametrize.py` | Tests covering yield fixtures, multi-input parametrize, `pytest.param` IDs, indirect parametrize, parametrized fixtures, and a skipped case |
| `requirements.txt` | Python dependencies |

## How to use

1. Install: `pip install -r requirements.txt`
2. Run: `pytest -v` — every test and parametrized case should pass (one case is skipped on purpose to demo `marks=pytest.mark.skip`).

Useful flags while exploring: `pytest -v -k palindrome`, `pytest -v test_parametrize.py::test_is_palindrome[simple_palindrome]` to run a single parametrized case by its `id=`.
