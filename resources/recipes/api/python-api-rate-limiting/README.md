# Python API Rate Limiting — Companion

Runnable companion for the StackPractices recipe: an in-memory `TokenBucket`, a minimal Flask app that applies it per-IP with a `Retry-After` header, and pytest coverage for burst, refill, rejection, and `retry_after` math.

## Files

- `token_bucket.py` — the limiter. Run `python token_bucket.py` for a quick demo.
- `flask_app.py` — Flask app applying the bucket per client IP. `python flask_app.py`, then hit `/api/data` 11+ times.
- `test_token_bucket.py` — 7 tests. `pytest test_token_bucket.py` (no Redis or Flask needed for the unit tests).

## Notes

In-memory buckets are per-process — use the Redis Lua variant from the recipe when you run more than one instance.

## Source

- [Python API Rate Limiting with Token Bucket — StackPractices](https://stackpractices.com/recipes/python-api-rate-limiting/)
- [Rate Limiting de API en Python — StackPractices](https://stackpractices.com/es/recipes/python-api-rate-limiting/)
