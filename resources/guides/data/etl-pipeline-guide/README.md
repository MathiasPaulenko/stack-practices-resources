# ETL Pipeline Guide — Companion Code

Runnable companion for the guide [ETL Pipelines: Extract, Transform, Load for Data Engineers](https://stackpractices.com/guides/etl-pipeline-guide/).

The core pipeline uses `sqlite3` so it runs anywhere; the same shapes work on Postgres with `%s` placeholders and `psycopg2`.

## Files

| File | Purpose |
|---|---|
| `etl_pipeline.py` | `IncrementalExtractor` (watermark, correct ordering), `DataTransformer` with `ValidationError`, `UpsertLoader` — the corrected versions of the guide's classes |
| `demo.py` | End-to-end run: 3 rows extracted, second run moves 0 rows (watermark), an upstream update loads only the changed row |
| `test_etl_pipeline.py` | pytest suite: incremental extraction, validator rejection, transform ordering, upsert idempotency |
| `daily_etl_dag.py` | Reference Airflow 2.x DAG (`schedule=`, S3 staging files between tasks, upsert via temp table) |
| `scd-type2.sql` | Slowly Changing Dimension Type 2 DDL + expire/insert statements (PostgreSQL) |

## Quick start

```bash
python demo.py          # end-to-end demo on in-memory sqlite
python -m pytest -q     # 4 tests
```

Expected demo output:

```
run 1: extracted=3 loaded=3
run 2: extracted=0 loaded=0
warehouse: 3 rows, total=63.0
run 3 (after update): extracted=1
order 1 now: qty=9 total=81.0
```

## Notes

- `daily_etl_dag.py` is a reference file: it needs a real Airflow 2.x environment with `production_db`, `aws_default`, and `warehouse` connections. It won't run standalone.
- Watermark extraction orders by the watermark column (then `rowid`) — see the guide for why ordering by id alone can skip rows when a batch truncates.
