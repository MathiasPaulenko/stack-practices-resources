"""Dynamic task mapping example for the StackPractices Airflow companion project."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pendulum
from airflow.decorators import dag, task

RAW_DIR = Path("/tmp/airflow_etl/raw")


def _ensure_files() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name in ("orders-2025-01-01.csv", "orders-2025-01-02.csv"):
        path = RAW_DIR / name
        if not path.exists():
            path.write_text("order_id,amount\n1,99.50\n")


@dag(
    dag_id="dynamic_mapping_example",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="0 2 * * *",
    catchup=False,
    default_args={"owner": "data-team", "retries": 2, "retry_delay": 30},
    tags=["example", "dynamic-mapping"],
)
def dynamic_mapping_example():
    @task
    def list_files():
        _ensure_files()
        return [str(p) for p in RAW_DIR.glob("orders-*.csv")]

    @task
    def process_file(path: str):
        print(f"Processing {path}")

    files = list_files()
    process_file.expand(path=files)


dag = dynamic_mapping_example()
