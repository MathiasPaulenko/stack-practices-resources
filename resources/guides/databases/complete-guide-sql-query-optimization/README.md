# Complete Guide to SQL Query Optimization - Code Examples

Runnable SQL and Python examples from the guide:
<https://stackpractices.com/guides/complete-guide-sql-query-optimization/>

## Files

| File | What it shows |
| --- | --- |
| `schema.sql` | PostgreSQL schema + seed data (users, orders, products, comments) — run first |
| `slow_queries.sql` | pg_stat_statements, pg_stat_activity, index/cache audits + MySQL slow log / Performance Schema |
| `indexes.sql` | Covering, partial, composite-order, functional and trigram indexes with EXPLAIN |
| `rewrites.sql` | Eight bad-vs-good rewrite pairs to diff with EXPLAIN ANALYZE |
| `materialized_view.sql` | MV creation, CONCURRENTLY refresh, MySQL summary-table + event workaround |
| `partitioning.sql` | Range and list partitions with visible partition pruning |
| `n_plus_one.py` | Offline sqlite3 demo: N+1 vs JOIN, with query counting |
| `pooling.py` | psycopg2 ThreadedConnectionPool + asyncpg pool skeleton |
| `redis_cache.py` | TTL-based query caching in Redis |

## Offline check

```bash
python n_plus_one.py 200
```

Prints the query count and timing for the N+1 loop vs the single JOIN.

## Live setup (PostgreSQL)

```bash
psql -d sandbox -f schema.sql
psql -d sandbox -f indexes.sql
psql -d sandbox -f materialized_view.sql
psql -d sandbox -f partitioning.sql
```

`slow_queries.sql` needs `pg_stat_statements` in
`shared_preload_libraries`. `pooling.py` and `redis_cache.py` need a
running PostgreSQL (and Redis for the latter) — see `requirements.txt`.
