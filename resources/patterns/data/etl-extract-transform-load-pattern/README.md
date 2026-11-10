# ETL Extract-Transform-Load — Companion Resources

Runnable companion for [ETL Extract-Transform-Load](https://stackpractices.com/patterns/etl-extract-transform-load-pattern/) on StackPractices.

## Files

| File | Purpose |
| --- | --- |
| `etl_pipeline.py` | `ETPipeline` class: extract → staging → transform → delete+insert load. Works with any SQLAlchemy engine. |
| `incremental_etl.py` | `IncrementalETL`: high-water-mark extraction persisted to `watermarks.json`. |
| `etl_customers.sql` | Same three stages in pure SQL (PostgreSQL 15+, uses `MERGE`). |
| `etl_dag.py` | Airflow DAG that orchestrates the pipeline stages (Airflow 2.4+, needs the postgres provider). |
| `CustomerEtlJob.java` | Spring Batch 5 reference job: `JdbcCursorItemReader` / `ItemProcessor` / `JdbcBatchItemWriter` with MERGE upsert, plus the `Customer` and `CustomerRowMapper` classes the article snippet references. |
| `demo.py` | End-to-end run on SQLite: seeds data, runs the pipeline twice to prove idempotency, then an incremental extraction. |
| `test_etl_pipeline.py` | pytest suite covering the full run, staging table naming, idempotent re-runs, and incremental watermarks. |

## Quick start

```bash
pip install pandas sqlalchemy pytest
python demo.py          # end-to-end run on SQLite
pytest test_etl_pipeline.py -v
```

`demo.py` creates `demo_source.db`, `demo_staging.db`, `demo_warehouse.db` and `demo_watermarks.json` in the working directory — safe to delete afterwards.

## Notes

- `etl_pipeline.py` uses a portable delete+insert upsert (`IN` with an expanding bind parameter) so it runs on SQLite, Postgres, and MySQL. The article shows the Postgres-specific `id = ANY(:ids)` variant.
- `etl_customers.sql` and `CustomerEtlJob.java` are PostgreSQL-dialect; adapt the upsert syntax for MySQL (`INSERT ... ON DUPLICATE KEY UPDATE`) or older SQL Server/Oracle. The Java file targets Spring Batch 5 (`JobRepository` + `PlatformTransactionManager`); the article also shows the Batch 4 `*BuilderFactory` variant.
- The DAG expects Airflow connections named `source_db`, `staging_db`, and `warehouse_db`.
