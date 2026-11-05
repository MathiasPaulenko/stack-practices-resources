# Production Pytest Configs

Companion resources for [Pytest in Production Guide](https://stackpractices.com/guides/complete-guide-pytest-production/).

## Contents

| File | Purpose |
| --- | --- |
| `conftest.py` | Scoped fixtures, xdist-aware DB fixture, factory fixture, hooks |
| `pytest.ini` | Markers, addopts, coverage, filterwarnings for production |
| `coveragerc` | Coverage source/omit/exclude config with fail_under = 80 |
| `factories.py` | factory_boy factories (User, Product, Order) |
| `tests.yml` | GitHub Actions workflow with postgres/redis services + matrix |

## Usage

1. Drop `conftest.py` into `tests/`, `pytest.ini` and `coveragerc` at repo root (rename to `.coveragerc`).
2. `pip install pytest pytest-xdist pytest-cov factory_boy`
3. `pytest -n auto` — workers get isolated databases via `PYTEST_XDIST_WORKER`.

See the guide for the scope decision table and troubleshooting.
