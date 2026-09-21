# Rate Limiting — Companion Resources

Companion code for the [Rate Limiting recipe](https://stackpractices.com/recipes/rate-limiting/) on StackPractices.com.

## What's included

| File | Language | Algorithm | Deployment |
|------|----------|-----------|------------|
| `token_bucket.py` | Python | Token bucket (bursts allowed) | In-memory, single process |
| `fixed_window_redis.js` | JavaScript | Fixed window + per-endpoint budgets | Redis, multi-instance |
| `SlidingWindow.java` | Java | Sliding window log (no boundary bursts) | In-memory, single process |
| `sliding_window_counter.py` | Python | Sliding window counter (weighted overlap) | In-memory, O(1) per key |

## Quick start

```bash
python token_bucket.py          # True
node -e "require('./fixed_window_redis.js')"  # requires redis package + server
javac SlidingWindow.java && java SlidingWindow  # true
```

## Pick your algorithm

- **Fixed window** (the JS one): start here — two Redis commands, correct enough for most APIs. The boundary lets through up to 2× at the window edge; at minute-scale windows that's rarely a problem.
- **Token bucket** (the Python one): when clients legitimately burst — sync clients, dashboards fanning out calls.
- **Sliding window** (the Java one): when the boundary burst actually costs money; costs a timestamp per request.

## Production notes

- Key on `user:{id}` or `api_key`, not IP — NATs punish innocents. Tightest limits on auth endpoints.
- Decide fail-open vs fail-closed for Redis outages *explicitly* — read traffic usually fails open, login/payment fails closed.
- Always return `429` + `Retry-After`; advertise `RateLimit-Limit/Remaining/Reset` so clients pace themselves.
- Distributed limiting needs a shared store — in-memory counters silently multiply the limit per instance.
