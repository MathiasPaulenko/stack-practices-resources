# Node.js Redis Caching — Companion

Runnable companion for the StackPractices recipe
[Node.js Redis Caching: Cache-Aside and TTL](https://stackpractices.com/recipes/nodejs-caching-redis/).

## What's inside

| File | Purpose |
|---|---|
| `app.js` | Express app with cache-aside + lock (stampede protection), tag-based invalidation, and a `/metrics` endpoint tracking hit rate |
| `docker-compose.yml` | Redis 7 (`allkeys-lru`, 128MB cap) plus Redis Commander UI |
| `package.json` | `express` + `ioredis` deps |

## Quick start

```bash
docker compose up -d
npm install
node app.js

curl http://localhost:3000/api/users/1      # database — first request
curl http://localhost:3000/api/users/1      # cache — second request
curl http://localhost:3000/metrics          # { hits: 1, misses: 1, hitRate: "50.0%" }
curl -X POST http://localhost:3000/api/users/1/refresh   # invalidate tag
```

Redis Commander runs at http://localhost:8081 to browse keys live.

## Notes

- `getOrSet` takes a `lock:${key}` with `SET NX EX` so a hot key expiring
  doesn't stampede the "database" — other callers retry after 100ms.
- `fetchUser` sleeps 150ms to simulate a slow query; the second call for
  the same id should come back in single-digit milliseconds.
- `invalidateTag("users")` wipes every key tagged `users` via `SMEMBERS` + `DEL`.

Source recipe: https://stackpractices.com/recipes/nodejs-caching-redis/
