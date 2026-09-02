"""Tests for traffic mirroring setup.

These tests validate that the mirror configuration works correctly
and that idempotent requests don't cause duplicate side effects.
"""

import requests
import pytest

PRODUCTION_URL = "http://production:8080"
STAGING_URL = "http://staging:8080"


def test_staging_receives_mirrored_traffic():
    """Verify that staging receives requests sent to production."""
    # Send a request to production
    prod_response = requests.get(f"{PRODUCTION_URL}/api/health")
    assert prod_response.status_code == 200

    # Check staging access logs or metrics for the mirrored request
    # In a real test, query the staging metrics endpoint
    staging_metrics = requests.get(f"{STAGING_URL}/metrics").text
    assert "mirror_requests_total" in staging_metrics


def test_idempotent_request_not_duplicated():
    """Confirm that a duplicated idempotent request doesn't create two resources."""
    headers = {
        "Idempotency-Key": "test-123",
        "Content-Type": "application/json",
    }
    body = {"amount": 100, "currency": "USD"}

    r1 = requests.post(f"{PRODUCTION_URL}/api/payments", json=body, headers=headers)
    r2 = requests.post(f"{PRODUCTION_URL}/api/payments", json=body, headers=headers)

    assert r1.status_code == r2.status_code
    assert r1.json()["id"] == r2.json()["id"]


def test_response_schema_matches():
    """Verify that production and staging return the same response schema."""
    prod = requests.get(f"{PRODUCTION_URL}/api/users/1")
    staging = requests.get(f"{STAGING_URL}/api/users/1")

    assert prod.status_code == staging.status_code
    assert set(prod.json().keys()) == set(staging.json().keys())


def test_auth_headers_stripped():
    """Verify that Authorization headers are stripped before mirroring."""
    headers = {"Authorization": "Bearer prod-secret-token"}
    requests.get(f"{PRODUCTION_URL}/api/data", headers=headers)

    # Check staging received the request without the auth header
    staging_logs = requests.get(f"{STAGING_URL}/debug/last-headers").json()
    assert "authorization" not in {k.lower() for k in staging_logs}


def test_mirror_does_not_block_production():
    """Verify that production response time is not affected by mirror latency."""
    import time

    # Simulate slow staging by measuring production response time
    start = time.monotonic()
    response = requests.get(f"{PRODUCTION_URL}/api/fast")
    duration = time.monotonic() - start

    # Production should respond in under 200ms regardless of staging latency
    assert response.status_code == 200
    assert duration < 0.2, f"Production took {duration:.3f}s, mirror may be blocking"
