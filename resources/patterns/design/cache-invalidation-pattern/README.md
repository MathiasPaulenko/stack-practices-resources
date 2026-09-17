# Cache Invalidation Pattern — Companion Code

Runnable versions of the invalidation strategies from the
[Cache Invalidation Pattern](https://stackpractices.com/patterns/cache-invalidation-pattern/)
resource on StackPractices.

## Files

| File | Description |
|------|-------------|
| `cache_invalidator.py` | Four Redis strategies in Python: TTL expiration, explicit invalidation on write, event-driven pub/sub (`CacheInvalidator`), and versioned keys |
| `cache-manager.ts` | TypeScript `CacheManager` with tag-based, versioned and write-through invalidation, plus a `PubSubInvalidator` for multi-instance setups |

## Requirements

- Python: `pip install redis` (use `fakeredis` for unit tests without a server)
- TypeScript: `redis` v4+ (`npm install redis`) and a Redis server
- `db` is a placeholder — wire it to your own data layer (ORM, query helper)

## Notes

- The Python client uses `decode_responses=True` so `get()` returns `str`.
  Without it, versioned keys break (`user:123:vb'1'`).
- `DEL` does not expand wildcards — `del("products:category:*")` only removes
  a literal key with that name. Use tag sets or `scan_iter` for grouped deletes.
