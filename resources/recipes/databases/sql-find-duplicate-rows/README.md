# Find and Remove Duplicate Rows in SQL

Runnable SQL scripts for detecting and safely removing duplicate rows. Detection scripts work on any engine; deletion variants are grouped by technique and engine. Always run the `SELECT` preview before any `DELETE`, and run cleanups inside a transaction or during a maintenance window on production data.

## Files

| File | Engine | What it shows |
|------|--------|---------------|
| `find-duplicates.sql` | Any | `GROUP BY` + `HAVING` detection, multi-column keys, case-insensitive and JSONB matching |
| `delete-duplicates-window-functions.sql` | PostgreSQL, MySQL 8+, SQLite 3.25+, SQL Server | Preview CTE, transactional delete with backup, verification, unique constraint |
| `delete-duplicates-mysql57.sql` | MySQL 5.7 | Self-join delete keeping `MIN(id)` — no window functions needed |
| `batch-delete-duplicates.sql` | PostgreSQL | `DO $$` loop deleting in chunks of 1000 with `pg_sleep` throttling, plus `ANALYZE`/`REINDEX`/`VACUUM FULL` follow-up |
| `merge-duplicates-before-delete.sql` | PostgreSQL | Merge non-null values into the canonical row before deleting |
| `case-insensitive-dedup.sql` | PostgreSQL | `LOWER(email)` partitioning plus a functional unique index to prevent recurrence |
| `dedup-across-tables.sql` | Any | `UNION ALL` detection across `users` and `archived_users`, archive cleanup |
| `clean-table-swap.sql` | PostgreSQL | `DISTINCT ON` clean copy + atomic table swap for heavily duplicated tables |

## Usage

Run the scripts against a copy of your data first:

```sql
CREATE TABLE users_dedup_test AS SELECT * FROM users;
```

Then adapt the `PARTITION BY` columns (the "uniqueness key") and the `ORDER BY` (which row to keep) to your schema.

## Key point

`ORDER BY` inside `ROW_NUMBER() OVER (...)` decides which row survives — oldest, newest, most complete or highest id. Pick it with business logic, not randomly, and add a unique constraint afterwards so duplicates can't come back.

Source: https://stackpractices.com/recipes/sql-find-duplicate-rows/
