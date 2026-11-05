# Redis Caching Strategies — Companion Examples

Runnable Python implementations of the five Redis caching patterns covered in
[Complete Guide to Redis Caching Strategies](https://stackpractices.com/guides/complete-guide-redis-caching-strategies/).

## Setup

```bash
pip install -r requirements.txt
redis-server  # or point REDIS_URL at your instance
```

## Files

- `caching_patterns.py` — all five patterns in one module:
  - `get_user` / `update_user` — cache-aside with TTL and invalidation
  - `get_user_safe` — cache-aside with a bounded stampede lock
  - `ReadThroughCache` — cache layer owns the miss path
  - `WriteThroughCache` — DB-then-cache synchronous writes
  - `write_behind_set` + `flush_worker` — async batched writes with logging
  - `refresh_ahead` — proactive refresh before TTL expiry via `scan_iter`
  - `set_with_jitter` — TTL jitter to avoid synchronized expirations

The examples expect a `db` object exposing `users.find_by_id()` / `users.update()`
— swap in your ORM or repository. Requires `redis-py >= 4.1` (for `scan_iter`
and `redis.cluster`).
