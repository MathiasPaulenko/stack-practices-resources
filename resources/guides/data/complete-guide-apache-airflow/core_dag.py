# dags/simple_dag.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "data-team",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
    "email_on_retry": False,
}

dag = DAG(
    "simple_etl",
    default_args=default_args,
    description="Simple ETL pipeline",
    schedule="0 2 * * *",  # Daily at 2 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["etl", "daily"],
)

extract = BashOperator(
    task_id="extract",
    bash_command="python /opt/etl/extract.py --date {{ ds }}",
    dag=dag,
)

def transform(**context):
    import pandas as pd
    date = context["ds"]
    df = pd.read_csv(f"/data/raw/{date}/orders.csv")
    df["total"] = df["subtotal"] + df["tax"]
    df.to_csv(f"/data/processed/{date}/orders.csv", index=False)

transform_task = PythonOperator(
    task_id="transform",
    python_callable=transform,
    dag=dag,
)

load = BashOperator(
    task_id="load",
    bash_command="python /opt/etl/load.py --date {{ ds }}",
    dag=dag,
)

extract >> transform_task >> load
