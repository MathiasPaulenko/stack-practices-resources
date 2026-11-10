"""Reference Airflow DAG for the daily ETL (Airflow 2.x).

Copy into your dags/ folder. Tasks hand data off through S3 staging files
(deterministic keys = execution date) so each task is independently
re-runnable — XComs are for small values only.
"""

from datetime import datetime, timedelta
from io import StringIO

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

STAGING_BUCKET = "data-lake"


def extract_orders(**context):
    pg_hook = PostgresHook(postgres_conn_id="production_db")
    ds = context["ds"]
    next_ds = (datetime.strptime(ds, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    df = pg_hook.get_pandas_df(
        "SELECT * FROM orders WHERE created_at >= %s AND created_at < %s",
        parameters=(ds, next_ds),
    )
    S3Hook(aws_conn_id="aws_default").load_string(
        df.to_csv(index=False),
        key=f"staging/orders/{ds}.csv",
        bucket_name=STAGING_BUCKET,
        replace=True,
    )
    return f"Extracted {len(df)} orders"


def transform_orders(**context):
    s3 = S3Hook(aws_conn_id="aws_default")
    ds = context["ds"]
    df = pd.read_csv(StringIO(s3.read_key(key=f"staging/orders/{ds}.csv",
                                          bucket_name=STAGING_BUCKET)))

    df["email"] = df["email"].str.lower().str.strip()
    df["order_total"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])

    s3.load_string(
        df.to_csv(index=False),
        key=f"processed/orders/{ds}.csv",
        bucket_name=STAGING_BUCKET,
        replace=True,
    )
    return f"Transformed {len(df)} orders"


def load_to_warehouse(**context):
    s3 = S3Hook(aws_conn_id="aws_default")
    ds = context["ds"]
    df = pd.read_csv(StringIO(s3.read_key(key=f"processed/orders/{ds}.csv",
                                          bucket_name=STAGING_BUCKET)))

    # Upsert via staging table so re-runs stay idempotent
    wh = PostgresHook(postgres_conn_id="warehouse")
    wh.run("CREATE TEMP TABLE orders_stage (LIKE fact_orders INCLUDING ALL)")
    with wh.get_conn() as c, c.cursor() as cur:
        from io import StringIO as SIO
        buf = SIO(df.to_csv(index=False, header=False))
        cur.copy_from(buf, "orders_stage", sep=",", columns=list(df.columns))
    wh.run(
        """INSERT INTO fact_orders SELECT * FROM orders_stage
           ON CONFLICT (order_id) DO UPDATE SET
             email = EXCLUDED.email,
             quantity = EXCLUDED.quantity,
             order_total = EXCLUDED.order_total"""
    )
    return f"Loaded {len(df)} orders"


with DAG(
    "daily_sales_etl",
    default_args=default_args,
    description="Daily sales ETL from production to warehouse",
    schedule="0 2 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["sales", "etl"],
) as dag:
    extract_task = PythonOperator(task_id="extract_orders", python_callable=extract_orders)
    transform_task = PythonOperator(task_id="transform_orders", python_callable=transform_orders)
    load_task = PythonOperator(task_id="load_to_warehouse", python_callable=load_to_warehouse)

    extract_task >> transform_task >> load_task
