# Throttling Pattern — Runnable Examples

Companion files for the [Throttling Pattern](https://stackpractices.com/patterns/throttling-pattern/):

- `token_bucket.py` — Python token bucket with `threading.Lock`, used by the `ThrottledAPI` wrapper
- `ThrottledService.java` — Spring service using Guava `RateLimiter` with `tryAcquire()`
- `sliding_window.js` — sliding-window log throttle per client
- `throttle.ts` — self-throttling client for a third-party API (waits for the next slot)
- `token_bucket.lua` — atomic token bucket for Redis, for multi-instance deployments

The Python and JavaScript files run standalone. The Lua script is meant for `EVAL`/`EVALSHA` against Redis: `KEYS[1]` token count, `KEYS[2]` last refill timestamp, `ARGV` = capacity, refill time baseline, now, rate.
