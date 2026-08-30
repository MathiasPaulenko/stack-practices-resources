"""Branching example for the StackPractices Airflow companion project."""
from __future__ import annotations

from datetime import datetime

import pendulum
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator


def _choose_branch(**kwargs):
    # In a real DAG this value comes from an upstream task or a sensor.
    row_count = kwargs["ti"].xcom_pull(task_ids="check_source", key="return_value") or 0
    return "full_transform" if int(row_count) > 100 else "sample_transform"


def _check_source():
    # Mock source check. Replace with a real query or sensor.
    return 150


def _full_transform():
    print("Running full transform")


def _sample_transform():
    print("Running sample transform")


@dag(
    dag_id="branching_example",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="0 2 * * *",
    catchup=False,
    default_args={"owner": "data-team", "retries": 2, "retry_delay": 30},
    tags=["example", "branching"],
)
def branching_example():
    check_source = PythonOperator(
        task_id="check_source",
        python_callable=_check_source,
    )

    branch = BranchPythonOperator(
        task_id="choose_branch",
        python_callable=_choose_branch,
    )

    full_transform = PythonOperator(
        task_id="full_transform",
        python_callable=_full_transform,
    )

    sample_transform = PythonOperator(
        task_id="sample_transform",
        python_callable=_sample_transform,
    )

    join = EmptyOperator(
        task_id="join",
        trigger_rule="one_success",
    )

    check_source >> branch >> [full_transform, sample_transform] >> join


dag = branching_example()
