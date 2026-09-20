"""Python snapshot examples — runnable with pytest.

Install:
    pip install pytest pytest-snapshot syrupy

First run (writes baselines):
    pytest --snapshot-create        # pytest-snapshot
    pytest --snapshot-update        # syrupy

Later runs compare against the stored baselines:
    pytest
"""

import json

from normalize_response import normalize_response


def build_api_response():
    return {
        "user": {
            "id": 1,
            "name": "Alice",
            "email": "alice@x.com",
            "role": "admin",
        },
        "metadata": {
            "version": "1.0",
            "page": 1,
            "per_page": 20,
        },
    }


def create_order(items):
    """Simulates an order creation with dynamic fields."""
    import uuid
    from datetime import datetime, timezone

    return {
        "id": str(uuid.uuid4()),
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "items": items,
        "status": "pending",
    }


# --- pytest-snapshot -------------------------------------------------------

def test_api_response(snapshot):
    """pytest-snapshot: assert_match compares text against a stored baseline."""
    response = build_api_response()
    snapshot.assert_match(json.dumps(response, indent=2))


def test_order_snapshot_normalized(snapshot):
    """Dynamic values are normalized to placeholders before snapshotting."""
    order = create_order(items=[{"productId": 1, "quantity": 2}])
    snapshot.assert_match(normalize_response(order))


# --- syrupy -----------------------------------------------------------------

def test_user_serialization(snapshot):
    """syrupy: `assert value == snapshot` uses the snapshot fixture."""
    user = {"id": 1, "name": "Alice", "email": "alice@x.com"}
    assert user == snapshot


def test_complex_data_structure(snapshot):
    data = {
        "users": [
            {"id": 1, "name": "Alice", "orders": [100, 101, 102]},
            {"id": 2, "name": "Bob", "orders": [200]},
        ],
        "pagination": {"page": 1, "total": 2},
    }
    assert data == snapshot
