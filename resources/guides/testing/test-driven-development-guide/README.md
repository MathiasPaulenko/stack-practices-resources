# Test-Driven Development — Companion

Runnable companion for the [Test-Driven Development guide](https://stackpractices.com/guides/test-driven-development-guide/) on StackPractices. Two artifacts from the guide made executable:

| Directory | What it is |
|-----------|------------|
| `python/` | The `ShoppingCart` built cycle by cycle in the guide, plus the full pytest suite — each test maps to one red-green-refactor loop. |
| `node/` | The Jest + supertest suite for `POST /api/transfers` from "TDD in Production". The `describe` block ships `.skip`ped: wire your Express app, `getAccount` and auth token into the marked stubs, then remove the skip. |

## Run it

```bash
# Python (5 tests)
cd python && pip install -r requirements.txt && pytest -x -q

# Node.js — after wiring your app into transfers.test.js
cd node && npm install && npm test
```

## What each file demonstrates

- `python/test_shopping_cart.py` — one test per TDD cycle: empty cart (red), add items, discount, edge case (invalid code), naming example with Arrange/Act/Assert comments.
- `node/transfers.test.js` — behavior-level test naming (`should reject...`), one assertion block per behavior, deterministic expectations.

Source guide: https://stackpractices.com/guides/test-driven-development-guide/
