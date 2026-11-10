# etl_dag.py — Airflow DAG orchestrating the ETLPipeline stages.
# Requires: apache-airflow, apache-airflow-providers-postgres, etl_pipeline.py
# on the Airflow PYTHONPATH. Uses Airflow connections: source_db, staging_db,
# warehouse_db. Hand-off between tasks happens through the staging table —
# only the staging table name travels via XCom, never row payloads.
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
import re

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_customers_daily',
    default_args=default_args,
    description='Daily ETL for customers table',
    schedule='0 2 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['etl', 'daily'],
)


def _pipeline(context):
    from etl_pipeline import ETLPipeline
    # Airflow run ids contain ':' and '+' — strip them for table-safe names
    safe_run_id = re.sub(r'\W', '', context['run_id'])[:12]
    source = PostgresHook(postgres_conn_id='source_db').get_sqlalchemy_engine()
    staging = PostgresHook(postgres_conn_id='staging_db').get_sqlalchemy_engine()
    warehouse = PostgresHook(postgres_conn_id='warehouse_db').get_sqlalchemy_engine()
    return ETLPipeline(source, staging, warehouse, run_id=safe_run_id)


def extract(**context):
    pipeline = _pipeline(context)
    pipeline.extract('customers', since=context['ds'])
    context['ti'].xcom_push(key='staging_table',
                           value=f"stg_customers_{pipeline.run_id}")


def transform(**context):
    pipeline = _pipeline(context)
    staging_table = context['ti'].xcom_pull(task_ids='extract', key='staging_table')
    df = pd.read_sql_table(staging_table, pipeline.staging)
    pipeline.transform(df).to_sql('tmp_customers', pipeline.staging,
                                  index=False, if_exists='replace')


def load(**context):
    pipeline = _pipeline(context)
    df = pd.read_sql_table('tmp_customers', pipeline.staging)
    pipeline.load(df, 'customers')
    context['ti'].xcom_push(key='rows_loaded', value=len(df))


def validate(**context):
    expected = context['ti'].xcom_pull(task_ids='load', key='rows_loaded')
    hook = PostgresHook(postgres_conn_id='warehouse_db')
    actual = hook.get_first("SELECT COUNT(*) FROM customers")[0]
    if actual < expected * 0.95:
        raise ValueError(
            f"Row count check failed: expected ~{expected}, got {actual}"
        )


def cleanup(**context):
    from sqlalchemy import text
    pipeline = _pipeline(context)
    staging_table = context['ti'].xcom_pull(task_ids='extract', key='staging_table')
    with pipeline.staging.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {staging_table}"))
        conn.execute(text("DROP TABLE IF EXISTS tmp_customers"))


for name, fn in [('extract', extract), ('transform', transform),
                 ('load', load), ('validate', validate), ('cleanup', cleanup)]:
    globals()[f'{name}_task'] = PythonOperator(
        task_id=name,
        python_callable=fn,
        dag=dag,
    )

extract_task >> transform_task >> load_task >> validate_task >> cleanup_task
