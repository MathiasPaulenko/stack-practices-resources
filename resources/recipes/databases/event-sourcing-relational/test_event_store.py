"""Tests for event_store.py.

Mocks psycopg2 so no database is required.
Run with: python -m pytest test_event_store.py -v
"""

import json
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from event_store import EventStore, ConcurrencyException, rebuild_account_balance


@pytest.fixture
def mock_conn():
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value.__enter__ = MagicMock(return_value=cursor)
    conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    return conn, cursor


def test_append_inserts_event(mock_conn):
    conn, cursor = mock_conn
    cursor.fetchone.return_value = (0,)

    store = EventStore(conn)
    store.append("acc-1", "Deposit", {"amount": 50})

    assert cursor.execute.call_count == 2
    conn.commit.assert_called_once()


def test_append_raises_on_version_mismatch(mock_conn):
    conn, cursor = mock_conn
    cursor.fetchone.return_value = (5,)

    store = EventStore(conn)
    with pytest.raises(ConcurrencyException):
        store.append("acc-1", "Deposit", {"amount": 50}, expected_version=3)


def test_append_allows_matching_version(mock_conn):
    conn, cursor = mock_conn
    cursor.fetchone.return_value = (3,)

    store = EventStore(conn)
    store.append("acc-1", "Deposit", {"amount": 50}, expected_version=3)
    conn.commit.assert_called_once()


def test_get_events_returns_sorted(mock_conn):
    conn, cursor = mock_conn
    cursor.fetchall.return_value = [
        ("Deposit", json.dumps({"amount": 50}), 1, "2026-01-01"),
        ("Withdrawal", json.dumps({"amount": 20}), 2, "2026-01-02"),
    ]

    store = EventStore(conn)
    events = store.get_events("acc-1")

    assert len(events) == 2
    assert events[0]["type"] == "Deposit"
    assert events[1]["type"] == "Withdrawal"


def test_get_events_with_from_version(mock_conn):
    conn, cursor = mock_conn
    cursor.fetchall.return_value = [
        ("Withdrawal", json.dumps({"amount": 20}), 2, "2026-01-02"),
    ]

    store = EventStore(conn)
    events = store.get_events("acc-1", from_version=1)

    assert len(events) == 1
    assert events[0]["version"] == 2


def test_save_snapshot_inserts(mock_conn):
    conn, cursor = mock_conn

    store = EventStore(conn)
    store.save_snapshot("acc-1", 5, {"balance": 100})

    conn.commit.assert_called_once()


def test_get_snapshot_returns_latest(mock_conn):
    conn, cursor = mock_conn
    cursor.fetchone.return_value = (5, json.dumps({"balance": 100}))

    store = EventStore(conn)
    snapshot = store.get_snapshot("acc-1")

    assert snapshot is not None
    assert snapshot["version"] == 5
    assert snapshot["state"]["balance"] == 100


def test_get_snapshot_returns_none_when_empty(mock_conn):
    conn, cursor = mock_conn
    cursor.fetchone.return_value = None

    store = EventStore(conn)
    snapshot = store.get_snapshot("acc-1")

    assert snapshot is None


def test_rebuild_account_balance_with_snapshot(mock_conn):
    conn, cursor = mock_conn

    # First call: get_snapshot
    cursor.fetchone.return_value = (3, json.dumps({"balance": 100}))
    # Second call: get_events fetchall
    cursor.fetchall.return_value = [
        ("Deposit", json.dumps({"amount": 50}), 4, "2026-01-04"),
    ]

    balance = rebuild_account_balance(conn, "acc-1")
    assert balance == 150


def test_rebuild_account_balance_without_snapshot(mock_conn):
    conn, cursor = mock_conn

    # First call: get_snapshot returns None
    cursor.fetchone.return_value = None
    # Second call: get_events fetchall
    cursor.fetchall.return_value = [
        ("Deposit", json.dumps({"amount": 50}), 1, "2026-01-01"),
        ("Withdrawal", json.dumps({"amount": 20}), 2, "2026-01-02"),
    ]

    balance = rebuild_account_balance(conn, "acc-1")
    assert balance == 30
