# Query Optimization — Companion Code

Runnable PostgreSQL companion for the [query-optimization recipe](https://stackpractices.com/recipes/query-optimization/). It gives you a database big enough for plan differences to matter, plus the exact `EXPLAIN (ANALYZE, BUFFERS)` exercises from the article.

## Files

| File | Purpose |
| --- | --- |
| `schema.sql` | Demo schema (customers, products, orders, order_items) seeded with ~200k orders and 500k items via `generate_series`. |
| `analyze.sql` | Side-by-side plan comparisons: Seq Scan vs Index Scan, covering index, N+1 vs JOIN, OFFSET vs keyset pagination, NOT IN vs NOT EXISTS. |
| `monitoring.sql` | Slow query log setup and `pg_stat_statements` queries for finding the most expensive and most unstable queries. |

## Usage

```bash
createdb query_demo
psql -d query_demo -f schema.sql   # takes a minute — seeds ~700k rows
psql -d query_demo -f analyze.sql
```

Read each `EXPLAIN (ANALYZE, BUFFERS)` output and watch the costly node disappear after each index or rewrite. For `monitoring.sql`, enable `pg_stat_statements` first (`CREATE EXTENSION pg_stat_statements;` as superuser, with `shared_preload_libraries` configured).

MySQL users: the recipe's concepts carry over, but this companion is PostgreSQL-specific.
