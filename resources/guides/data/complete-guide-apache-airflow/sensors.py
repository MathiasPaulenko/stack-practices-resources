from airflow.sensors.filesystem import FileSensor
from airflow.sensors.s3 import S3KeySensor
from airflow.sensors.sql import SqlSensor
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.sensors.date_time import DateTimeSensor

# Wait for a file to appear
wait_for_file = FileSensor(
    task_id="wait_for_file",
    filepath="/data/raw/{{ ds }}/orders.csv",
    poke_interval=60,  # Check every 60 seconds
    timeout=3600,      # Give up after 1 hour
    mode="poke",       # or "reschedule" to free worker slot
    dag=dag,
)

# Wait for S3 object
wait_for_s3 = S3KeySensor(
    task_id="wait_for_s3",
    bucket_key="raw/{{ ds }}/orders.parquet",
    bucket_name="my-data-bucket",
    aws_conn_id="aws_default",
    poke_interval=300,
    timeout=7200,
    dag=dag,
)

# Wait for SQL condition
wait_for_data = SqlSensor(
    task_id="wait_for_data",
    sql="SELECT COUNT(*) FROM staging WHERE load_date = '{{ ds }}' AND status = 'ready'",
    conn_id="warehouse",
    poke_interval=60,
    timeout=3600,
    dag=dag,
)

# Wait for another DAG to complete
wait_for_upstream = ExternalTaskSensor(
    task_id="wait_for_upstream",
    external_dag_id="ingestion_pipeline",
    external_task_id="load_to_warehouse",
    check_existence=True,
    poke_interval=300,
    timeout=7200,
    dag=dag,
)
