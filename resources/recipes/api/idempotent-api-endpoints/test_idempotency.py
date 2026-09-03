"""Tests for idempotent API endpoints — Python FastAPI implementation.

Covers duplicate requests, concurrent requests, TTL expiry, and error recovery.
Run with: pytest test_idempotency.py -v
"""
import pytest
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient

from python_fastapi import app, idempotency_store, IDEMPOTENCY_TTL


@pytest.fixture
def client():
    idempotency_store.clear()
    return TestClient(app)


@pytest.fixture
def short_ttl(monkeypatch):
    """Set TTL to 1 second for expiry tests."""
    import python_fastapi
    monkeypatch.setattr(python_fastapi, "IDEMPOTENCY_TTL", 1)
    return python_fastapi


def make_headers():
    return {"Idempotency-Key": str(uuid.uuid4())}


def test_missing_key_returns_400(client):
    r = client.post("/orders", json={"customer_id": "c1", "amount": 10})
    assert r.status_code == 400
    assert "Idempotency-Key" in r.json()["detail"]


def test_invalid_key_format_returns_400(client):
    r = client.post(
        "/orders",
        json={"customer_id": "c1", "amount": 10},
        headers={"Idempotency-Key": "not-a-uuid"},
    )
    assert r.status_code == 400
    assert "Invalid" in r.json()["detail"]


def test_first_request_succeeds(client):
    headers = make_headers()
    r = client.post("/orders", json={"customer_id": "c1", "amount": 10}, headers=headers)
    assert r.status_code == 200
    assert r.json()["cached"] is False
    assert r.json()["status"] == "completed"


def test_duplicate_returns_cached(client):
    headers = make_headers()
    r1 = client.post("/orders", json={"customer_id": "c1", "amount": 10}, headers=headers)
    r2 = client.post("/orders", json={"customer_id": "c1", "amount": 10}, headers=headers)
    assert r1.json()["cached"] is False
    assert r2.json()["cached"] is True
    assert r1.json()["id"] == r2.json()["id"]


def test_concurrent_one_wins_other_gets_409(client):
    """Test concurrent request protection.

    With TestClient (synchronous), we simulate concurrency by manually
    setting the processing state before the second request.
    """
    headers = make_headers()
    # First request
    r1 = client.post("/orders", json={"customer_id": "c1", "amount": 10}, headers=headers)
    assert r1.status_code == 200
    # Manually set processing state to simulate in-flight request
    idempotency_store[headers["Idempotency-Key"]] = {
        "status": "processing",
        "timestamp": time.time(),
        "order_id": None,
    }
    # Second request with same key should get 409
    r2 = client.post("/orders", json={"customer_id": "c1", "amount": 10}, headers=headers)
    assert r2.status_code == 409


def test_expired_key_allows_new_request(client, short_ttl):
    headers = make_headers()
    client.post("/orders", json={"customer_id": "c1", "amount": 10}, headers=headers)
    time.sleep(1.1)
    r = client.post("/orders", json={"customer_id": "c1", "amount": 10}, headers=headers)
    assert r.json()["cached"] is False


def test_different_keys_create_different_orders(client):
    h1 = make_headers()
    h2 = make_headers()
    r1 = client.post("/orders", json={"customer_id": "c1", "amount": 10}, headers=h1)
    r2 = client.post("/orders", json={"customer_id": "c1", "amount": 10}, headers=h2)
    assert r1.json()["id"] != r2.json()["id"]


def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
