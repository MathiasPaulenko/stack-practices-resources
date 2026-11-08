"""Airflow DAG from the pipeline design document — Airflow 2.x.

References the callables/scripts the design doc specifies; fill in the
extraction and load implementations in your ETL package.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def extract_orders_from_api(**context):
    """Pull the daily orders snapshot from the Orders API.

    Implement pagination, OAuth2 client credentials, and the retry/backoff
    policy documented in the design document's source table.
    """
    raise NotImplementedError("implement per design doc section 2")


default_args = {
    "owner": "data-platform",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "email": ["data-platform@example.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "sla": timedelta(minutes=90),
}

with DAG(
    "orders_etl_pipeline",
    default_args=default_args,
    schedule="0 2 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["etl", "orders", "production"],
) as dag:
    extract_orders = PythonOperator(
        task_id="extract_orders_api",
        python_callable=extract_orders_from_api,
    )

    stage_orders = BashOperator(
        task_id="stage_orders",
        bash_command="cd /opt/etl && python stage_orders.py --date {{ ds }}",
    )

    run_dbt = BashOperator(
        task_id="run_dbt_transforms",
        bash_command=(
            "cd /opt/dbt && dbt run --select int_orders_dedup "
            "int_orders_enriched fct_order_metrics"
        ),
    )

    quality_check = BashOperator(
        task_id="quality_checks",
        bash_command="cd /opt/dbt && dbt test --select fct_order_metrics",
    )

    load_redshift = BashOperator(
        task_id="load_redshift",
        bash_command="cd /opt/etl && python load_redshift.py --date {{ ds }}",
    )

    export_s3 = BashOperator(
        task_id="export_s3",
        bash_command="cd /opt/etl && python export_s3.py --date {{ ds }}",
    )

    extract_orders >> stage_orders >> run_dbt >> quality_check >> load_redshift >> export_s3
