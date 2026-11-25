# Database Schema Evolution — Companion Resources

Runnable files for the [Database Schema Evolution](https://stackpractices.com/recipes/schema-evolution/) recipe on StackPractices.

## Files

| File | What it is |
|------|------------|
| `expand_contract_postgres.sql` | The three-phase expand-contract rename (`ADD` → dual-write → `DROP`) on PostgreSQL with batched backfill. |
| `pt_online_schema_change.sh` | Percona's `pt-online-schema-change` invocation for adding an index on a large MySQL table without locking. Credentials come from env vars. |
| `gh_ost_online_change.sh` | GitHub's `gh-ost` invocation for the same class of change; binlog-based sync, no triggers. Fails fast if `MYSQL_PASSWORD` is unset. |
| `liquibase_changelog.xml` | Liquibase changelog with the expand-contract sequence expressed as three changeSets (add column → backfill → drop old column). |
| `V1_2__add_user_preferences.sql` | Flyway-style versioned migration creating a `user_preferences` table. |
| `not_null_and_fk_safely.sql` | Adding `NOT NULL`, `CHECK`, and `FOREIGN KEY` constraints on live PostgreSQL tables using the `NOT VALID` + `VALIDATE` two-step. |
| `split_column_trigger.sql` | Splitting `full_name` into `first_name`/`last_name` with a plpgsql dual-write trigger that keeps both representations in sync. |
| `migration_session_settings.sql` | Session guards (`lock_timeout`, `statement_timeout`), replication-lag check, and `ANALYZE` after backfills. |

## Usage

- **PostgreSQL**: run the `.sql` files against a staging copy first — `psql -f expand_contract_postgres.sql`. Run `migration_session_settings.sql` at the top of each migration session.
- **MySQL**: `bash gh_ost_online_change.sh` or `bash pt_online_schema_change.sh` with `MYSQL_HOST`/`MYSQL_USER`/`MYSQL_PASSWORD`/`MYSQL_DB` exported.
- **Flyway/Liquibase**: drop the SQL/XML files into your migration directory and let the tool apply them in order.

Every script assumes it may be re-run: use `IF (NOT) EXISTS` where your version supports it and always test rollback in staging before production.
