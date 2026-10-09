"""End-to-end demo: commands -> event store -> projections -> queries.

Requires PostgreSQL. Point DATABASE_URL at a database you can write to:

    export DATABASE_URL=postgresql://user:pass@localhost/eventstore
    python main.py
"""

import os
import uuid

from event_store import EventStore
from handlers import CommandHandler
from projectors import AccountProjector, AccountStatsProjector, ProjectorManager
from queries import AccountQueryService
from snapshots import SnapshotStore, load_aggregate

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://user:pass@localhost/eventstore"
)


def main():
    store = EventStore(DATABASE_URL)
    snapshot_store = SnapshotStore(DATABASE_URL)
    handler = CommandHandler(store)
    queries = AccountQueryService(store.Session)
    projector_manager = ProjectorManager(
        [AccountProjector(store.Session), AccountStatsProjector(store.Session)]
    )

    account_id = str(uuid.uuid4())

    # Write side — commands append events to the store
    handler.handle(account_id, lambda acc: acc.create("Alice", 1000))
    handler.handle(account_id, lambda acc: acc.deposit(500, "Salary"))
    handler.handle(account_id, lambda acc: acc.withdraw(200, "Groceries"))

    # Read side — feed stored events to projections
    for event in store.get_events(account_id):
        projector_manager.handle(event)

    print("Account:", queries.get_account(account_id))
    print("Transactions:", queries.get_transactions(account_id))

    # Snapshot, then reload via snapshot + tail replay
    loaded = load_aggregate(account_id, store, snapshot_store)
    snapshot_store.save_snapshot(
        account_id,
        loaded.version,
        {
            "owner_name": loaded.owner_name,
            "balance": loaded.balance,
            "status": loaded.status,
            "version": loaded.version,
        },
    )
    reloaded = load_aggregate(account_id, store, snapshot_store)
    print("Reloaded balance:", reloaded.balance)


if __name__ == "__main__":
    main()
