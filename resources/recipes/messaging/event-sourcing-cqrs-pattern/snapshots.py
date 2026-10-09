import json
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from aggregate import BankAccount
from event_store import Base, EventStore


class SnapshotStore:
    """Store aggregate snapshots to avoid replaying all events."""

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)  # creates the snapshots table too
        self.Session = sessionmaker(bind=self.engine)

    def save_snapshot(self, aggregate_id: str, version: int, state: dict):
        session = self.Session()
        try:
            session.execute(
                text(
                    """INSERT INTO snapshots (aggregate_id, version, state, created_at)
                       VALUES (:id, :ver, :state, NOW())
                       ON CONFLICT (aggregate_id) DO UPDATE
                       SET version = :ver, state = :state, created_at = NOW()"""
                ),
                {"id": aggregate_id, "ver": version, "state": json.dumps(state)},
            )
            session.commit()
        finally:
            session.close()

    def get_snapshot(self, aggregate_id: str) -> Optional[tuple]:
        session = self.Session()
        try:
            result = session.execute(
                text("SELECT version, state FROM snapshots WHERE aggregate_id = :id"),
                {"id": aggregate_id},
            ).fetchone()
            if result:
                return result[0], json.loads(result[1])
            return None
        finally:
            session.close()


def load_aggregate(
    aggregate_id: str, event_store: EventStore, snapshot_store: SnapshotStore
):
    """Load from snapshot, then replay only newer events."""
    snapshot = snapshot_store.get_snapshot(aggregate_id)
    if snapshot:
        version, state = snapshot
        account = BankAccount(aggregate_id)
        account.__dict__.update(state)
        events = event_store.get_events(aggregate_id, from_version=version)
        for event in events:
            account.apply(event)
            account.version = event.version
        return account
    events = event_store.get_events(aggregate_id)
    return BankAccount.from_events(aggregate_id, events)
