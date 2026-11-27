# Analyze and Optimize SQL Indexes — Companion Scripts

Runnable PostgreSQL scripts that accompany the recipe
[Analyze and Optimize SQL Indexes with EXPLAIN](https://stackpractices.com/recipes/sql-index-optimization-analysis/).

## Files

| Script | What it does |
|--------|--------------|
| `explain-analyze-baseline.sql` | Baseline EXPLAIN ANALYZE + composite index for a slow query |
| `find-unused-indexes.sql` | Indexes with zero scans, with sizes |
| `find-duplicate-indexes.sql` | Indexes covering identical columns |
| `partial-index.sql` | Partial index on active rows only |
| `covering-index.sql` | INCLUDE index for Index Only Scans |
| `expression-index.sql` | Indexes on `LOWER(email)` and `DATE_TRUNC` |
| `drop-index-safely.sql` | Sized check + `DROP INDEX CONCURRENTLY` |
| `reindex-and-analyze.sql` | REINDEX CONCURRENTLY + statistics refresh |
| `monitoring-weekly.sql` | Weekly index-health queries for cron |
| `hypothetical-index-hypopg.sql` | Test index impact with HypoPG |

## Usage

Requires PostgreSQL 11+ (`INCLUDE` and `REINDEX CONCURRENTLY` need PG11+/12+).
`hypothetical-index-hypopg.sql` needs the [HypoPG](https://hypopg.readthedocs.io/) extension.

```bash
psql -d your_db -f explain-analyze-baseline.sql
```

All drop/reindex scripts use `CONCURRENTLY` so they are safe to run on
live tables, but always monitor index usage for at least a week before
dropping anything in production.

## More resources

- Recipe (ES): https://stackpractices.com/es/recipes/sql-index-optimization-analysis/
- Full resource library: https://mathiaspaulenko.github.io/stack-practices-resources/
