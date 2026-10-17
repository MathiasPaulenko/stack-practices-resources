# Rate Limiting for API Security

Companion resources for the [Rate Limiting for API Security recipe](https://stackpractices.com/recipes/rate-limiting-security/) on StackPractices.

Rate limiting as a defense layer: atomic Redis token bucket, tiered Express middleware, edge limits in Nginx, and a burst-test script.

## Files

| File | Description |
|------|-------------|
| `token_bucket.lua` | Atomic token-bucket check-and-decrement Lua script for Redis |
| `rate_limiter.py` | Python caller wrapping the Lua script with a login rate-limit helper |
| `express_limiter.js` | Express middleware factory with tiered auth/API limits (rate-limiter-flexible) |
| `nginx-rate-limit.conf` | Nginx `limit_req` zones: strict on `/api/auth/`, lenient on `/api/` |
| `test_limits.sh` | Burst-test script that fires requests and shows when 429 kicks in |

## Requirements

- Redis 5+ running locally (`redis-server` or `docker run -p 6379:6379 redis`)
- Python: `pip install redis`
- Node.js: `npm install rate-limiter-flexible redis`

## Quick start

```bash
# 1. Test the atomic limiter directly in redis-cli
redis-cli --eval token_bucket.lua rl:test , 5 1 0 60

# 2. Python example — prints allowed/limited per attempt
python rate_limiter.py

# 3. Verify a live endpoint
./test_limits.sh https://api.example.com/api/auth/login
```

## Notes

- Always run the check-and-decrement atomically (Lua or a library that does it internally). Two-step read/write lets bursts slip through under concurrency.
- Key on something the attacker can't rotate cheaply: `IP + account` for auth, user ID or API key for reads.
- Pair with your WAF — rate limiting slows attackers, it doesn't authenticate them.
