# Write-Behind Cache Pattern — Companion Code

Runnable versions of the write-behind implementations from the
[Write-Behind Cache Pattern](https://stackpractices.com/patterns/write-behind-cache-pattern/)
resource on StackPractices.

## Files

| File | Description |
|------|-------------|
| `write_behind_cache.py` | Python `WriteBehindCache` with a durable dirty set in Redis, atomic flush takeover via `RENAME`, batch upsert example, and a fakeredis demo |
| `write-behind-cache.ts` | TypeScript `WriteBehindCache` with the same Redis-backed dirty set, `multi()` pipelined writes, and a Postgres `ON CONFLICT` batch writer |

## Requirements

- Python: `pip install redis` (`pip install fakeredis` to run the demo without a server)
- TypeScript: `redis` v4+ (`npm install redis`) and a Redis server
- `db` is a placeholder — wire it to your own data layer (psycopg, pg, Prisma)

## Notes

- The dirty set is stored in Redis (`writebehind:dirty`), not in process
  memory, so an application crash does not lose the flush queue. Redis
  itself still needs persistence (AOF `everysec` or RDB+AOF) to bound the
  data-loss window if the server goes down.
- `RENAME dirty → flushing` atomically takes the pending set, so writes
  that arrive during a flush are picked up by the next cycle.
- Keep value TTLs well above the worst-case flush lag — a key that expires
  or is evicted while still dirty is a silently lost write.
