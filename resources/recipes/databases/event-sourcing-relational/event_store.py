"""Event sourcing implementation for PostgreSQL.

Provides an EventStore class with optimistic concurrency, event replay,
and snapshot support. Requires psycopg2.

Usage:
    import psycopg2
    conn = psycopg2.connect("dbname=test user=postgres")
    store = EventStore(conn)
    store.append("acc-1", "Deposit", {"amount": 50})
    balance = rebuild_account_balance(conn, "acc-1")
"""

import json
from datetime import datetime, timezone
from uuid import uuid4


class ConcurrencyException(Exception):
    """Raised when optimistic concurrency check fails."""


class EventStore:
    def __init__(self, conn):
        self.conn = conn

    def append(self, aggregate_id, event_type, payload, expected_version=None):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM events WHERE aggregate_id = %s",
                (aggregate_id,)
            )
            current_version = cur.fetchone()[0]

            if expected_version is not None and current_version != expected_version:
                raise ConcurrencyException(
                    f"Expected {expected_version}, found {current_version}"
                )

            cur.execute("""
                INSERT INTO events (id, aggregate_id, event_type, payload, version, occurred_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (str(uuid4()), aggregate_id, event_type, json.dumps(payload),
                  current_version + 1, datetime.now(timezone.utc)))
            self.conn.commit()

    def get_events(self, aggregate_id, from_version=0):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT event_type, payload, version, occurred_at
                FROM events WHERE aggregate_id = %s AND version > %s
                ORDER BY version
            """, (aggregate_id, from_version))
            return [{
                "type": row[0], "payload": json.loads(row[1]),
                "version": row[2], "occurred_at": row[3]
            } for row in cur.fetchall()]

    def save_snapshot(self, aggregate_id, version, state):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO snapshots (aggregate_id, version, state, created_at)
                VALUES (%s, %s, %s, %s)
            """, (aggregate_id, version, json.dumps(state),
                  datetime.now(timezone.utc)))
            self.conn.commit()

    def get_snapshot(self, aggregate_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT version, state FROM snapshots
                WHERE aggregate_id = %s ORDER BY version DESC LIMIT 1
            """, (aggregate_id,))
            row = cur.fetchone()
            if row:
                return {"version": row[0], "state": json.loads(row[1])}
            return None


def rebuild_account_balance(conn, account_id):
    store = EventStore(conn)
    snapshot = store.get_snapshot(account_id)
    balance = 0
    from_version = 0

    if snapshot:
        balance = snapshot["state"].get("balance", 0)
        from_version = snapshot["version"]

    events = store.get_events(account_id, from_version)
    for event in events:
        if event["type"] == "Deposit":
            balance += event["payload"]["amount"]
        elif event["type"] == "Withdrawal":
            balance -= event["payload"]["amount"]
    return balance
