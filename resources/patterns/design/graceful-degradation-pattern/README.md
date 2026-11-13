# Graceful Degradation Pattern — Companion Files

Runnable graceful degradation implementations in three languages. Each one wraps
an unreliable call with a three-step fallback ladder: **primary call →
TTL-bounded cache → default value**, and returns a `ServiceResult` that tells the
caller exactly how degraded the response is (`healthy`, `degraded`, or `down`).

Source article: <https://stackpractices.com/patterns/graceful-degradation-pattern/>

## Files

| File | Language | Notes |
|------|----------|-------|
| `graceful_degradation.py` | Python 3.8+ | `call_with_fallback` accepts an optional `fallback_fn`; `aggregate` degrades each service independently |
| `gracefulDegradation.mjs` | Node.js 18+ | Same ladder with a `Map`-backed cache; `callWithFallback(service, primary, fallback, default, cacheKey)` |
| `GracefulDegradation.java` | Java 11+ | `record`-based `ServiceResult` with `healthy`/`degraded`/`down` factories |

## Run

```bash
python graceful_degradation.py
node gracefulDegradation.mjs
javac GracefulDegradation.java && java GracefulDegradation
```

Each program simulates a product page where `recommendations` and `inventory`
fail while `product_details` and `reviews` succeed. Expected output: the page
assembles anyway, with the failing services marked `DEGRADED` and served from
defaults or cache.

## Notes

- The in-memory cache and the 300-second TTL are for demonstration. In
  production, use a shared cache (Redis/Memcached) and a TTL per data type —
  recommendations tolerate hours, prices tolerate minutes.
- The examples catch broad exceptions for brevity. Real code should only treat
  dependency failures (timeouts, connection errors, 5xx, open circuit breakers)
  as degradation triggers; a 404 or validation error deserves a real failure.
