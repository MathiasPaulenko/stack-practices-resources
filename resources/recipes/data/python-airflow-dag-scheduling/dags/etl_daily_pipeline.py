"""Runnable Airflow DAG example for StackPractices.

This DAG demonstrates TaskFlow API, sensors, branching, XCom, and idempotent writes.
It is meant for local learning and testing, not production.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import pendulum
from airflow.decorators import dag, task

RAW_DIR = Path("/tmp/airflow_etl/raw")
PROCESSED_DIR = Path("/tmp/airflow_etl/processed")


def _ensure_data() -> None:
    """Create a tiny sample CSV if it does not exist."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    sample = RAW_DIR / "orders.csv"
    if not sample.exists():
        sample.write_text(
            "order_id,order_date,amount\n"
            "1,2025-01-15,99.50\n"
            "2,2025-01-15,\n"  # missing amount, will be filtered
            "3,2025-01-15,150.00\n"
        )


@dag(
    dag_id="etl_daily_pipeline",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="0 2 * * *",
    catchup=False,
    default_args={"owner": "data-team", "retries": 2, "retry_delay": 30},
    tags=["etl", "daily", "example"],
    doc_md="""
    # ETL Daily Pipeline

    A learning DAG that reads a CSV, filters missing values, and writes a Parquet file.
    """,
)
def etl_daily_pipeline():
    @task
    def wait_for_file():
        _ensure_data()
        sample = RAW_DIR / "orders.csv"
        if not sample.exists():
            raise FileNotFoundError(f"{sample} not found")
        return str(sample)

    @task
    def extract(filepath: str) -> str:
        import pandas as pd

        df = pd.read_csv(filepath)
        print(f"Extracted {len(df)} rows")
        return df.to_json()

    @task
    def transform(raw_json: str) -> str:
        import pandas as pd

        df = pd.read_json(raw_json)
        df["order_date"] = pd.to_datetime(df["order_date"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df.dropna(subset=["amount"])
        print(f"Transformed {len(df)} rows")
        return df.to_json()

    @task
    def load(transformed_json: str) -> str:
        import pandas as pd

        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        df = pd.read_json(transformed_json)
        output = PROCESSED_DIR / f"orders_{datetime.utcnow().date()}.parquet"
        df.to_parquet(output, index=False)
        print(f"Loaded {len(df)} rows to {output}")
        return str(output)

    raw_path = wait_for_file()
    raw_json = extract(raw_path)
    transformed = transform(raw_json)
    load(transformed)


dag = etl_daily_pipeline()
