from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

dag = DAG("pipeline_with_quality_checks", schedule="0 2 * * *", start_date=datetime(2026, 1, 1), catchup=False, max_active_runs=1)

def extract(**context):
    import pandas as pd
    hook = PostgresHook(postgres_conn_id="source_db")
    df = hook.get_pandas_df("SELECT * FROM source WHERE date = %(ds)s", parameters={"ds": context["ds"]})
    df.to_csv(f"/data/raw/{context['ds']}/orders.csv", index=False)
    return len(df)

import pandera as pa

def make_validator(path_tpl, schema):
    def _v(**context):
        import pandas as pd
        df = pd.read_csv(path_tpl.format(ds=context["ds"]))
        schema.validate(df, lazy=True)
    return _v

raw_schema = pa.DataFrameSchema({
    "order_id": pa.Column(int, checks=pa.Check.unique(), nullable=False),
    "status": pa.Column(str, checks=pa.Check.isin(["pending", "processing", "shipped", "completed", "cancelled"])),
})

def transform(**context):
    import pandas as pd
    df = pd.read_csv(f"/data/raw/{context['ds']}/orders.csv")
    df["total"] = df["subtotal"] + df["tax"] + df["shipping"]
    df.to_csv(f"/data/processed/{context['ds']}/orders.csv", index=False)

processed_schema = pa.DataFrameSchema({
    "order_id": pa.Column(int, checks=pa.Check.unique(), nullable=False),
    "total": pa.Column(float, checks=pa.Check.ge(0), nullable=False),
})

extract_task = PythonOperator(task_id="extract", python_callable=extract, dag=dag)
validate_raw = PythonOperator(task_id="validate_raw", python_callable=make_validator("/data/raw/{ds}/orders.csv", raw_schema), dag=dag)
transform_task = PythonOperator(task_id="transform", python_callable=transform, dag=dag)
validate_processed = PythonOperator(task_id="validate_processed", python_callable=make_validator("/data/processed/{ds}/orders.csv", processed_schema), dag=dag)

extract_task >> validate_raw >> transform_task >> validate_processed
