# Object Pool Pattern

Runnable companion files for [Object Pool Pattern](https://stackpractices.com/patterns/object-pool-pattern/).

Fixed-size pool of expensive connections in three languages: pre-warmed objects, `acquire()`/`release()` with fail-fast exhaustion, and a safe checkout wrapper (`with`, try/finally, `withConnection`) so objects always return to the pool.

## Files

| File | Language | Notes |
| --- | --- | --- |
| `connection_pool.py` | Python 3.8+ | `queue.Queue`-backed pool, `PoolExhaustedError`, `pool.pooled()` context manager |
| `ConnectionPool.java` | Java 11+ | `BlockingQueue` pool, bounded `poll()` instead of blocking `take()` |
| `connection-pool.js` | Node 14+ | Array-backed pool, `PoolExhaustedError`, async `withConnection(fn)` helper |

## Run

```bash
python connection_pool.py
javac ConnectionPool.java && java ConnectionPool
node connection-pool.js
```

Each demo acquires an object, queries, releases, then acquires again — the second checkout reuses the same object (no new "(expensive)" line).

## Notes

- All three pools fail fast instead of blocking forever when exhausted — an unbounded `acquire` turns a full pool into a hung app.
- The pooled `DatabaseConnection` is a stub. Swap in a real client (psycopg, JDBC, pg/mysql2) and add a validation ping on checkout for production use.
