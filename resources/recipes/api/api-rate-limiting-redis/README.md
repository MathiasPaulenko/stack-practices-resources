# API Rate Limiting with Redis — Companion Resources

Runnable companion for the recipe **[Implement API Rate Limiting with Redis](https://stackpractices.com/recipes/api-rate-limiting-redis/)** on StackPractices.

## Files

| File | Purpose |
|---|---|
| `TokenBucket.ts` | Atomic token bucket for Redis. The refill math runs inside a Lua script and time comes from `redis.call('TIME')`, so every app node measures against the same clock — no drift between instances. |
| `SlidingWindow.ts` | Sliding window counter on a Redis sorted set (`ZADD`/`ZREMRANGEBYSCORE`/`ZCARD` in one pipeline). Stricter than token bucket; it tracks exact request timestamps. |
| `rateLimit.ts` | Express middleware that emits IETF `RateLimit-*` headers on every response and `429` + `Retry-After` when the bucket is empty. |
| `TierConfig.ts` | Per-user tier configuration: `free`/`pro`/`enterprise` buckets with their own capacity and refill rate, keyed as `rate:{tier}:{userId}`. |

## Quick start

```bash
npm install express ioredis
docker run -d -p 6379:6379 redis:7
```

```typescript
import express from 'express';
import { Redis } from 'ioredis';
import { TokenBucketLimiter } from './TokenBucket';
import { rateLimit } from './rateLimit';

const app = express();
const limiter = new TokenBucketLimiter(new Redis());

app.use('/api/public', rateLimit(limiter, { capacity: 100, refillRate: 10 }));
app.use('/api/premium', rateLimit(limiter, { capacity: 1000, refillRate: 100 }));
app.listen(3000);
```

## Verify it works

Fire requests until the bucket drains and watch the 11th request return `429` with `Retry-After`:

```bash
for i in $(seq 1 11); do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/api/public; done
```

## Production notes

- Wrap Redis calls in a circuit breaker and fail open — a Redis outage shouldn't become an API outage.
- Every mutating command must set `EXPIRE`/`PEXPIRE`, or inactive clients keep keys alive forever.
- On Redis Cluster, use hash tags (`rate:{tenantId}:…`) so a client's keys land on the same slot.
