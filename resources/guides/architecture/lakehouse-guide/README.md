# Lakehouse Architecture — Companion Pipeline Scripts

Runnable scripts for the medallion pipeline described in the [Lakehouse Architecture guide](https://stackpractices.com/guides/lakehouse-guide/) on StackPractices.

## Contents

| File | Purpose |
|------|---------|
| `bronze_to_silver_delta.py` | Clean raw JSON events and `MERGE` them into a Delta Silver table (idempotent, keyed on `event_id`) |
| `silver_to_gold_delta.py` | Daily business aggregates as a Delta Gold table |
| `delta_maintenance.py` | Weekly maintenance: `OPTIMIZE`, `Z-ORDER`, `VACUUM`, and `symlink_format_manifest` for Athena |
| `iceberg_setup.py` | Iceberg table with hidden partitioning + partition evolution (day → hour, no rewrite) |
| `hudi_upsert.py` | Record-level upserts and incremental reads with Apache Hudi |
| `spark_submit.sh` | The full pipeline as `spark-submit` commands on EMR/YARN |
| `requirements.txt` | Python dependencies |

## Usage

```bash
# Install locally (or submit to EMR/Databricks)
pip install -r requirements.txt

# End-to-end medallion pipeline (edit S3 paths first)
./spark_submit.sh s3://lakehouse/bronze/events/dt=2026-07-11/ \
    s3://lakehouse/silver/events/ s3://lakehouse/gold/daily_metrics/
```

Each script accepts the table paths as positional arguments; the defaults match the guide's scenario (`s3://lakehouse/...`).

## Notes

- The Delta merge is keyed on `event_id`, so re-running Bronze→Silver for the same day updates rows instead of duplicating them.
- `VACUUM` is irreversible — 168h (7 days) is a sane default; check your audit requirements first.
- `delta_maintenance.py` generates the `symlink_format_manifest` that Athena needs to read Delta tables.
