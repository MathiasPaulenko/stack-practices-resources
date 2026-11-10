# ETL Job Runbook — Companion Resources

Runnable companion for [ETL Job Runbook Template](https://stackpractices.com/docs/etl-job-runbook-template/) on StackPractices.

## Files

| File | Purpose |
| --- | --- |
| `runbook/etl-job-runbook-template.md` | Fill-in version of the runbook shown in the article — every field is a `<placeholder>`. |
| `scripts/health-checks.sh` | Executable pre-run health check: scheduler/worker pods, source API, staging bucket, warehouse, dbt compile, previous run state. Env-var driven; missing tools report SKIP, not FAIL. Exits non-zero on failures so it can gate a cron or pipeline step. |
| `monitoring/airflow-commands.md` | Airflow 2.x CLI cheat sheet verified against the official reference, including the commands that no longer exist (`tasks run`, `tasks logs`, `connections set`, `tasks duration`) and what to use instead. |
| `monitoring/dbt-tests-schema.yml` | dbt `schema.yml` for `fct_orders`: the column tests the `quality_checks` task runs in failure scenario F4 (not_null, unique, accepted_values, freshness support). |
| `checklists/game-day-drill.md` | Quarterly drill checklist: five injectable failure scenarios mapped to the runbook's F1–F6 entries, scoring criteria, and post-drill update rules. |

## Quick start

```bash
# Run the health checks against your environment
DAG_ID=orders_etl_pipeline \
SOURCE_API_HEALTH_URL=https://api.example.com/health \
STAGING_BUCKET=example-staging/orders \
WAREHOUSE_HOST=analytics-cluster \
DBT_PROJECT_DIR=/opt/dbt \
bash scripts/health-checks.sh
```

Every check degrades to `SKIP` when its tool or env var is missing, so the script also works as a checklist you read through.

## Notes

- All Airflow commands target **Airflow 2.x** (`tasks clear` for re-runs, `dags backfill`, UI for logs). Airflow 3 removed `dags backfill` and renames several subcommands — see `monitoring/airflow-commands.md`.
- The SQL snippets assume PostgreSQL/Redshift dialect (`stv_*` tables). Adjust for your warehouse.
