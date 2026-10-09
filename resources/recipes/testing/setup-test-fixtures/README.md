# Set Up Test Fixtures — Companion Resources

Companion files for [Set Up Test Fixtures (pytest, Jest, JUnit)](https://stackpractices.com/recipes/setup-test-fixtures/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `conftest.py` | Shared pytest fixtures: simple, yield/teardown, parametrized, factory, session scope |
| `test_fixtures.py` | Tests consuming conftest fixtures + `@pytest.mark.parametrize` |
| `factories.js` | Jest factory helpers with deterministic counter IDs |
| `fixtures.test.js` | Jest lifecycle: `beforeAll`/`afterAll`, `beforeEach` resets, factory usage |
| `TestFixtures.java` | JUnit 5 lifecycle: `@BeforeAll`/`@BeforeEach`, factory method, `@ParameterizedTest` |
| `requirements.txt` | Python dependencies |

## How to use

1. Python: `pip install -r requirements.txt` then `pytest -v`.
2. JavaScript: `npm install --save-dev jest` then `npx jest fixtures.test.js` (ESM: add `"type": "module"`).
3. Java: add `junit-jupiter` to test scope and run `TestFixtures`.

Keep mutable state at function/per-test scope and reset in `beforeEach` — order-dependent failures come from skipped resets.