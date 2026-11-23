# Redis Cache Invalidation in Node.js

Runnable companion for the StackPractices recipe
[Implement Redis Cache Invalidation in Node.js](https://stackpractices.com/recipes/nodejs-redis-cache-invalidation/).

## What's inside

- **`cache.js`** — the invalidation helpers from the recipe, written as a small library: TTL write (`cacheProduct`), explicit `DEL` + repopulate (`updateProduct`), `SCAN`+`DEL` pattern clearing with dedup and per-batch pipelines (`invalidatePattern`), pub/sub broadcast and L1 subscriber (`publishInvalidation`, `createInvalidationSubscriber`), and a stampede lock (`getProductWithLock`). The Redis client is injected, so the same code runs on `ioredis` or `ioredis-mock`.
- **`server.js`** — Express demo wired to a real Redis on `localhost:6379`. An in-memory product map stands in for the database; a local `Map` plays the L1 cache that stays in sync through the `cache:invalidate` pub/sub channel.
- **`test.js`** — `node:test` suite running end-to-end against `ioredis-mock`. No Redis server needed: TTL writes, explicit deletion, pattern clearing, pub/sub propagation to L1, and the lock are all covered.

## Run

```bash
npm install
npm test        # 4/4 tests against ioredis-mock
npm start       # needs a real Redis on localhost:6379
```

## Endpoints (with `npm start` running)

| Route | What it shows |
|---|---|
| `GET /products/:id` | L1 → Redis → DB cache-aside read with stampede lock |
| `PUT /products/:id` | Write-through update + pub/sub invalidation broadcast |
| `DELETE /products/:id` | Explicit deletion + broadcast |
| `POST /invalidate-products` | `SCAN`+`DEL` pattern wipe of every `product:*` key |
| `GET /l1` | Current contents of the in-memory L1 cache |

Hit `PUT /products/1` with `{"price": 69}` twice in a row and watch `GET /l1`:
the pub/sub event clears the L1 entry between calls.
