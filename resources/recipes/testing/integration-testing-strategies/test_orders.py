import pytest
import requests
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="module")
def db_engine():
    with PostgresContainer("postgres:15") as postgres:
        yield create_engine(postgres.get_connection_url())


@pytest.fixture
def api_client():
    return requests.Session()


def test_create_order_and_query(db_engine, api_client):
    response = api_client.post("http://localhost:8000/orders", json={
        "items": [{"sku": "abc", "quantity": 2}],
        "customer_id": "cust-123"
    })
    assert response.status_code == 201
    order_id = response.json()["id"]

    with db_engine.connect() as conn:
        result = conn.execute(
            "SELECT status, total FROM orders WHERE id = %s",
            (order_id,)
        )
        row = result.fetchone()
        assert row.status == "pending"
        assert row.total == 49.99
