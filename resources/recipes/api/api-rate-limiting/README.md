# API Rate Limiting — Companion Resources

Runnable companion for the recipe **[API Rate Limiting](https://stackpractices.com/recipes/api-rate-limiting/)** on StackPractices.

## Files

| File | Purpose |
|---|---|
| `token_bucket.lua` | Atomic token bucket for Redis — the read-check-update runs inside Redis so concurrent requests can't race the counter (the weakness of `hgetall` + `hset` in application code). |
| `rate_limiter.py` | Python wrapper: `RateLimiter.token_bucket()` (Lua-backed, atomic), `RateLimiter.sliding_window()` (sorted set), and `token_bucket_fail_open()` for Redis-down tolerance. |
| `express-rate-limit.js` | Express middleware: sliding window keyed by API key → user ID → IP, RFC 9457 problem+json 429s, `X-RateLimit-*` headers, fail-open on Redis errors. |
| `test_rate_limiter.py` | pytest suite covering the recipe's four scenarios: enforcement (N+1), window reset, Redis failover, and distributed consistency. |

## Quick start — Python

```bash
pip install redis fakeredis pytest
docker run -d -p 6379:6379 redis:7   # or skip and let fakeredis cover tests
pytest test_rate_limiter.py -v
```

```python
import redis
from rate_limiter import RateLimiter

limiter = RateLimiter(redis.Redis(host='localhost', port=6379))
result = limiter.token_bucket("user:u_4812", capacity=100, refill_rate=1.6)
if not result.allowed:
    return {"error": "rate limited", "retry_after": result.retry_after}, 429
```

## Quick start — Express

```bash
npm install express redis
node -e "
const express = require('express');
const { rateLimit } = require('./express-rate-limit');
const app = express();
app.use((req, res, next) => { req.id = 'req_demo'; next(); });
app.use(rateLimit({ limit: 5, windowSec: 60 }));
app.get('/ping', (req, res) => res.json({ ok: true }));
app.listen(3000);
" &
for i in 1 2 3 4 5 6 7; do curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/ping; done
# 200 ×5, then 429 with application/problem+json + Retry-After
```

## Notes

- `REDIS_URL` overrides the default `redis://localhost:6379` in the middleware.
- The Lua script takes `now` as an argument — pass the caller's clock, not `TIME`, so tests can control time.
- `token_bucket_fail_open` is the deliberate policy: a dead limiter allows traffic and logs, it doesn't take the API down. Invert it (fail closed) only where unlimited access is worse than downtime.
