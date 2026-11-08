"""Airflow DAG with automatic OpenLineage extraction.

Requires the openlineage-airflow provider and this in airflow.cfg
(or the AIRFLOW__OPENLINEAGE__TRANSPORT env var):

    [openlineage]
    transport = {"type": "http", "url": "http://marquez:5000"}
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_with_lineage',
    default_args=default_args,
    schedule='0 2 * * *',
    start_date=datetime(2026, 1, 1),
    tags=['etl', 'lineage'],
)


def extract(**context):
    # The Airflow extractor reads XCom for dataset info
    context['ti'].xcom_push(key='inputs', value=[
        {"namespace": "postgres://source", "name": "shop.customers"}
    ])
    context['ti'].xcom_push(key='outputs', value=[
        {"namespace": "postgres://warehouse", "name": "warehouse.customers"}
    ])
    # Actual ETL logic here
    pass


extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag,
)
