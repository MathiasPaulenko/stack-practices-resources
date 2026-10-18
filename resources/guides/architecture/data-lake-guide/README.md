# Data Lake Medallion Pipeline

Runnable companion to the [Data Lake vs Data Warehouse — Architecture Guide](https://stackpractices.com/guides/data-lake-guide/) on StackPractices.

Two ways to run the same Bronze → Silver → Gold flow: a laptop-friendly pandas/pyarrow pipeline, and the Spark + Delta Lake jobs from the guide's e-commerce scenario.

## Files

| File | Description |
|------|-------------|
| `medallion_pipeline.py` | Self-contained pipeline: generates synthetic clickstream events, lands them in Bronze (JSON), cleans/dedupes/partitions into Silver (hive-style Parquet `event_date=YYYY-MM-DD/`), and aggregates daily metrics into Gold. |
| `bronze_to_silver.py` | The Spark job from the guide: clean raw JSON → Delta table partitioned by `event_date`, then `OPTIMIZE` + `VACUUM`. |
| `delta_example.py` | Delta Lake essentials: ACID write, time travel (`versionAsOf`), schema evolution (`mergeSchema`). |
| `requirements.txt` | pandas + pyarrow for the runnable pipeline; pyspark + delta-spark optional for the Spark examples. |

## Run it (no Spark needed)

```bash
pip install -r requirements.txt
python medallion_pipeline.py
```

You'll get a `lake/` directory with:

```text
lake/
├── bronze/events/dt=2026-10-18/events.json
├── silver/events/event_date=2026-10-18/*.parquet
└── gold/daily_events.parquet
```

The Silver output shows the two things the guide stresses: nulls and duplicates removed (Silver is validated), and data partitioned by the column queries filter on.

## Run the Spark version

```bash
pip install pyspark delta-spark
spark-submit bronze_to_silver.py   # points at s3:// paths — adjust for local
python delta_example.py            # writes ./lake/silver/orders
```

## Key idea

Bronze is append-only (your replay source), Silver is typed and deduplicated (where most queries go), Gold exists per consumer. If a Gold table has no consumer, delete it.
