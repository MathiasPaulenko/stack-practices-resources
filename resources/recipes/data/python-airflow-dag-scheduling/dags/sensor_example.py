"""Sensor example for the StackPractices Airflow companion project."""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import pendulum
from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.sensors.python import PythonSensor

WATCH_DIR = Path("/tmp/airflow_etl/raw")


def _file_exists() -> bool:
    WATCH_DIR.mkdir(parents=True, exist_ok=True)
    return (WATCH_DIR / "orders.csv").exists()


def _process():
    sample = WATCH_DIR / "orders.csv"
    print(f"Processing {sample}")


@dag(
    dag_id="file_sensor_example",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="0 2 * * *",
    catchup=False,
    default_args={"owner": "data-team", "retries": 2, "retry_delay": 30},
    tags=["example", "sensor"],
)
def file_sensor_example():
    wait_for_file = PythonSensor(
        task_id="wait_for_file",
        python_callable=_file_exists,
        mode="reschedule",
        poke_interval=30,
        timeout=60 * 60,
    )

    process = PythonOperator(
        task_id="process",
        python_callable=_process,
    )

    wait_for_file >> process


dag = file_sensor_example()
