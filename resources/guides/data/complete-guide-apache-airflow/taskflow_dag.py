# dags/taskflow_dag.py — Modern TaskFlow API
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    schedule="0 2 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["etl", "taskflow"],
)
def orders_pipeline():

    @task
    def extract(date: str) -> dict:
        import requests
        resp = requests.get(f"https://api.example.com/orders?date={date}")
        return resp.json()

    @task
    def transform(raw_data: dict) -> list[dict]:
        orders = []
        for order in raw_data["orders"]:
            orders.append({
                "order_id": order["id"],
                "total": order["subtotal"] + order["tax"] + order["shipping"],
                "status": order["status"],
            })
        return orders

    @task
    def load(orders: list[dict], date: str) -> None:
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        hook = PostgresHook(postgres_conn_id="warehouse")
        for order in orders:
            hook.run(
                "INSERT INTO orders (order_id, total, status, load_date) VALUES (%s, %s, %s, %s) "
                "ON CONFLICT (order_id) DO UPDATE SET total=EXCLUDED.total, status=EXCLUDED.status",
                parameters=(order["order_id"], order["total"], order["status"], date),
            )

    raw = extract("{{ ds }}")
    cleaned = transform(raw)
    load(cleaned, "{{ ds }}")
