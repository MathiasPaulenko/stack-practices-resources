"""Airflow DAG that runs the dbt pipeline daily.

Airflow >= 2.4 (schedule= parameter; schedule_interval is deprecated).
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG("dbt_pipeline", schedule="@daily", start_date=datetime(2025, 1, 1))

# dbt build runs models + tests + snapshots + seeds in DAG order (dbt >= 1.2)
dbt_build = BashOperator(
    task_id="dbt_build",
    bash_command="cd /opt/dbt && dbt build --select marts.*",
    dag=dag,
)
