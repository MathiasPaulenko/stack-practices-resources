# API Rate Limiting — Companion Resources

Rate limiting implementations for the [API Rate Limiting guide](https://stackpractices.com/guides/api-rate-limiting-guide/).

| File | What it shows |
|------|---------------|
| `token_bucket.py` | In-process token bucket (bursts up to capacity) |
| `sliding_window.py` | Sliding window log (exact) and counter (O(1) memory) |
| `rate_limit.lua` | Atomic token bucket for Redis (`EVAL`) |
| `nginx_rate_limit.conf` | Gateway-level limits: per-IP + per-API-key zones |
| `fastapi_rate_limit.py` | FastAPI + `fastapi-limiter` Redis setup |
