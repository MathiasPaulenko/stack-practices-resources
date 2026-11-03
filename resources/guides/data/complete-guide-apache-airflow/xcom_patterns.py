# XCom passes small data between tasks. For large data, use external storage.

@task
def extract():
    # Small data: return directly (passed via XCom)
    return {"total_orders": 1500, "total_revenue": 45000.00}

@task
def validate(stats):
    if stats["total_orders"] < 1:
        raise ValueError("No orders found")
    return stats

@task
def report(stats):
    print(f"Orders: {stats['total_orders']}, Revenue: ${stats['total_revenue']}")

# For large data, use external storage (S3, GCS)
@task
def extract_large(date: str):
    import pandas as pd
    from airflow.providers.postgres.hooks.postgres import PostgresHook
    hook = PostgresHook(postgres_conn_id="warehouse")
    df = hook.get_pandas_df(f"SELECT * FROM orders WHERE date = '{date}'")
    path = f"/tmp/orders_{date}.parquet"
    df.to_parquet(path)
    return path  # Pass the path, not the data

@task
def transform_large(path):
    import pandas as pd
    df = pd.read_parquet(path)
    # Transform...
    return path
