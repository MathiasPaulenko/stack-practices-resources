# Cache-Aside Pattern — Companion Code

Runnable versions of the cache-aside implementations from the
[Cache-Aside Pattern](https://stackpractices.com/patterns/cache-aside-pattern/)
resource on StackPractices.

## Files

| File | Description |
|------|-------------|
| `cache_aside.py` | Python `CacheAside` backed by Redis: TTL on every key, invalidate-on-write, and a `SET NX PX` fill lock so a cold-cache stampede produces one database load instead of N |
| `cache-aside.ts` | TypeScript `CacheAside` for redis v4: promise deduplication (single-flight) for concurrent misses, `setEx` TTL, invalidate-on-write |

## Requirements

- Python: `pip install redis` (`pip install fakeredis` to run the demo without a server)
- TypeScript: `redis` v4+ (`npm install redis`) and a Redis server
- `db` is a placeholder — wire it to your own data layer (psycopg, pg, Prisma)

## Notes

- Invalidation deletes the key instead of updating it: the next read
  self-heals, and there is only one write path to keep in sync.
- The TTL is the safety net for missed invalidation events — it is not a
  substitute for deleting the key on writes.
- Both implementations protect the miss path: the Python version uses a
  short-lived lock and the TypeScript one reuses the in-flight promise.
