# Database Query Tuning Checklist — SQL Triage Pack

Companion resources for the doc [Database Query Tuning Checklist](https://stackpractices.com/docs/database-query-tuning-checklist/).

## Files

| File | What it is |
| --- | --- |
| `top-slow-queries.sql` | `pg_stat_statements` reports: top queries by total time and worst cache-hit ratio; slow-log enable; MySQL `performance_schema` equivalent |
| `index-audit.sql` | Index health audit: usage per table, unused indexes, tables doing heavy seq scans, selectivity query, duplicate index detection |

## Usage

```bash
# PostgreSQL — run inside psql against the target database
psql -d mydb -f top-slow-queries.sql
psql -d mydb -f index-audit.sql

# Install the extension once (if pg_stat_statements errors)
# CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

## Gotchas

- `pg_stat_statements` resets on restart — run reports before rebooting or snapshot them.
- `idx_scan = 0` doesn't always mean "safe to drop": check unique constraints (`indisunique`) and indexes used only during batch windows.
- Never leave `long_query_time = 0` / `log_min_duration_statement = 0` on in production — log flood.
