# Build an ETL Pipeline with pandas and Parquet

Runnable companion code for the StackPractices recipe:
[Build an ETL Pipeline with pandas and Parquet](https://stackpractices.com/recipes/python-pandas-etl-pipeline/)

A complete extract-transform-load pipeline in a single file: reads CSV/JSON
sources, coerces types, validates data quality, and writes partitioned Parquet
with `snappy` compression. Includes retry logic for flaky sources, incremental
append with deduplication, and schema enforcement.

## Contents

| File | What it does |
|---|---|
| `etl_pipeline.py` | Full pipeline: `extract_csv`, `extract_json`, `extract_with_retry`, `extract_and_merge`, `transform`, `transform_with_validation`, `enforce_schema`, `load_partitioned`, `load_incremental`, `run_pipeline_safe` |
| `requirements.txt` | `pandas` + `pyarrow` |

## Setup and run

```bash
pip install -r requirements.txt
python etl_pipeline.py
```

The script generates a small `data/raw/orders.csv` (including a negative
amount, a bad numeric value, and a duplicate ID so you can see validation
working), then runs the pipeline and writes partitioned output under
`data/processed/orders/year=*/month=*/`.

Read a partition back:

```python
import pandas as pd
df = pd.read_parquet("data/processed/orders/year=2025/month=02")
```

## Notes

- `errors="coerce"` turns bad values into `NaN` instead of raising — combined
  with the nullable `Int64` dtype so missing integers survive the cast.
- Retries wrap `extract` only: transform errors are deterministic, I/O errors
  are not.
- Swap `compression="snappy"` for `"zstd"` when storage cost matters more
  than write speed.
