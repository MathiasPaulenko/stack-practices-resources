from typing import Callable

from aggregate import BankAccount
from event_store import EventStore


class CommandHandler:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def handle(self, aggregate_id: str, command: Callable[[BankAccount], None]):
        # Load aggregate from event store
        events = self.event_store.get_events(aggregate_id)
        account = BankAccount.from_events(aggregate_id, events)

        # Execute command (raises events)
        command(account)

        # Persist new events
        pending = account.get_pending_events()
        if pending:
            self.event_store.append(
                aggregate_id, pending, account.version - len(pending)
            )
            account.clear_pending_events()

        return account
