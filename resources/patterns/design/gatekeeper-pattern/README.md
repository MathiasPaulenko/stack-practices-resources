# Gatekeeper Pattern — Companion Resources

Runnable examples for the [Gatekeeper pattern](https://stackpractices.com/patterns/gatekeeper-pattern/) on StackPractices.

The pattern puts one inspection point at the system edge: blocked paths, rate limiting, injection screening, and JWT authentication run before any request touches a backend service. Rejections map to distinct codes (403 / 429 / 400 / 401) so attack patterns surface in monitoring.

## Files

| File | What it shows |
|------|---------------|
| `gatekeeper.py` | Framework-free `Gatekeeper` class in Python — four inspection layers plus a minimal HS256 JWT signer/verifier on stdlib `hmac` |
| `test_gatekeeper.py` | pytest suite: 8 tests covering every rejection path, public-route auth skipping, and forged/expired tokens |
| `gatekeeper.js` | The same validator in JavaScript, with per-layer `check*()` methods middleware stacks can call individually |
| `gatekeeper.test.js` | `node:test` suite: 10 tests for the class plus the Express-style pipeline |
| `express_app.js` | The layers as Express-style middleware with a zero-dependency `(req, res, next)` engine — drop-in for real Express |

## Run it

```bash
# Python demo + tests
python gatekeeper.py
python -m pytest test_gatekeeper.py -v

# JavaScript demo + tests (Node 18+)
node gatekeeper.js
node --test gatekeeper.test.js

# Express-style server
node express_app.js   # then curl http://localhost:3000/api/public/products
```

## Key takeaways

- Cheapest rejection first: path blocking, then rate limiting, then injection screening, then JWT — a forged token never burns a signature check it doesn't need.
- Public routes (`/api/public/*`, `/health`) skip *authentication* only — every other layer still applies.
- The JWT secret comes from `GATEKEEPER_JWT_SECRET`; the demo files use a `dev-secret-for-demo-only` fallback, the article examples fail fast instead — never ship either pattern with a real secret in the file.
- `checkAuth` attaches the verified payload to `req.user`, so downstream handlers get identity for free.
- Rate-limit counters live in process memory here; swap the map for Redis before running more than one replica.

CI: `.github/workflows/test.yml` runs both test suites on every change to this folder.
