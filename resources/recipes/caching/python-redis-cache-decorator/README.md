# Cache Function Results with Redis and TTL in Python

Runnable companion for the recipe:
https://stackpractices.com/recipes/python-redis-cache-decorator/

## Contents

- `cache_decorator.py` — `@cached` decorator (deterministic key generation from the function signature, JSON serialization, configurable TTL, `wrapper.cache_invalidate`), `async_cached` variant, and `invalidate_tag` helper. The `__main__` block runs a hit/miss/invalidation smoke test against a local Redis.

## Requirements

- Python 3.10+
- A running Redis instance (`docker run -p 6379:6379 redis:7` is the quickest option)

## Setup and run

```bash
pip install -r requirements.txt
python cache_decorator.py
```

Expected output:

```text
{'id': '42', 'value': 'computed-42'}
{'id': '42', 'value': 'computed-42'}
{'id': '42', 'value': 'computed-42'}
OK: cache hit, miss, and invalidation all behave as expected
```

The second call is served from Redis (the counter stays at 1); the call after `cache_invalidate` recomputes.
