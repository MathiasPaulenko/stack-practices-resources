# Caching with Redis — Companion

Runnable companion for the [Redis caching recipe](https://stackpractices.com/recipes/caching-redis/) on StackPractices. The cache-aside helpers and stampede protection from the recipe, organized per stack:

| File | What it is |
|------|------------|
| `python/cache_aside.py` | The `cached()` decorator, session store and manual invalidation. |
| `python/stampede.py` | Lease-lock + probabilistic early-refresh stampede defenses. |
| `node/cache.js` | `getCached()` helper, invalidation and INCR/EXPIRE rate limiter (ioredis). |
| `java/CacheClient.java` | Jedis pool client (`get`/`setex`). Spring's `@Cacheable`/`@CacheEvict` are shown in the recipe body — they live in the service layer, not a standalone file. |

## Requirements

- Redis running locally (`docker run -p 6379:6379 redis:7`)
- Python: `pip install redis`
- Node: `npm install ioredis`
- Java: `redis.clients:jedis` on the classpath

## Run it

```bash
cd python && python cache_aside.py && python stampede.py
cd ../node && node cache.js
```

Source recipe: https://stackpractices.com/recipes/caching-redis/
