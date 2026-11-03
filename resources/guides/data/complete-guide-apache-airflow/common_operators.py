from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.amazon.aws.operators.s3 import S3CopyObjectOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.empty import EmptyOperator

# Bash: run shell commands
run_script = BashOperator(
    task_id="run_script",
    bash_command="python /opt/jobs/process.py --date {{ ds }} --env prod",
)

# Python: call Python functions
process_data = PythonOperator(
    task_id="process_data",
    python_callable=my_function,
    op_kwargs={"date": "{{ ds }}", "batch_size": 1000},
)

# Snowflake: execute SQL
run_sql = SnowflakeOperator(
    task_id="run_sql",
    sql="MERGE INTO orders USING staging_orders ON orders.id = staging_orders.id WHEN MATCHED THEN UPDATE ...",
    snowflake_conn_id="snowflake_prod",
)

# Spark: submit Spark jobs
spark_job = SparkSubmitOperator(
    task_id="spark_job",
    conn_id="spark_default",
    application="/opt/jobs/transform.py",
    application_args=["--input", "s3://data/{{ ds }}/"],
    conf={"spark.executor.memory": "4g", "spark.executor.cores": "2"},
)

# Email: send notifications
notify = EmailOperator(
    task_id="notify",
    to="data-team@company.com",
    subject="Pipeline completed for {{ ds }}",
    html_content="<p>Daily ETL completed successfully.</p>",
)

# Empty: no-op for grouping (was DummyOperator before Airflow 2.4)
start = EmptyOperator(task_id="start")
end = EmptyOperator(task_id="end")
