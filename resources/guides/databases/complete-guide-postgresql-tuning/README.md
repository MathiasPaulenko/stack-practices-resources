# PostgreSQL Tuning Configs

Companion resources for [Complete Guide to PostgreSQL Tuning](https://stackpractices.com/guides/complete-guide-postgresql-tuning/).

## Contents

| File | Purpose |
| --- | --- |
| `postgresql-4gb.conf` | Tuning profile for a 4GB dedicated host |
| `postgresql-16gb.conf` | Tuning profile for a 16GB dedicated host |
| `postgresql-64gb.conf` | Tuning profile for a 64GB dedicated host |
| `pgbouncer.ini` | PgBouncer connection pool config (transaction mode, SCRAM auth) |
| `pgbench-baseline.sh` | Baseline benchmark script — run before and after tuning |
| `monitoring-queries.sql` | All monitoring queries from the guide, ready to run |

## Usage

1. Pick the config profile closest to your host RAM and merge it into `postgresql.conf` (via `ALTER SYSTEM` or config include).
2. Restart PostgreSQL, then run `pgbench-baseline.sh mydb before` — tune one parameter, restart or reload, run it again as `after` and compare.
3. Keep `monitoring-queries.sql` handy for cache hit ratio, bloat, index usage, and live query checks.

See the guide for the reasoning behind each value and per-table autovacuum tuning.
