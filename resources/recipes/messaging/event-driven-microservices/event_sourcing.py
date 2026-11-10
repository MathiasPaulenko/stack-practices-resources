"""Event sourcing demo: an order aggregate rebuilt by replaying events.

Companion runnable for https://stackpractices.com/recipes/event-driven-microservices/
No dependencies — run `python event_sourcing.py`.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Event:
    aggregate_id: str
    event_type: str
    payload: dict
    version: int


class EventStore:
    """In-memory append-only store. Swap for PostgreSQL/EventStoreDB in production."""

    def __init__(self) -> None:
        self._events: Dict[str, List[Event]] = {}

    def append(self, event: Event) -> None:
        stream = self._events.setdefault(event.aggregate_id, [])
        expected = len(stream) + 1
        if event.version != expected:
            raise ValueError(f"version conflict: expected {expected}, got {event.version}")
        stream.append(event)

    def load(self, aggregate_id: str) -> List[Event]:
        return list(self._events.get(aggregate_id, []))


@dataclass
class OrderAggregate:
    order_id: str
    status: str = "pending"
    events: List[Event] = field(default_factory=list)

    def apply(self, event: Event) -> None:
        if event.event_type == "order_placed":
            self.status = "placed"
        elif event.event_type == "payment_received":
            self.status = "paid"
        elif event.event_type == "order_cancelled":
            self.status = "cancelled"
        self.events.append(event)

    def _record(self, store: EventStore, event_type: str, payload: dict) -> Event:
        event = Event(self.order_id, event_type, payload, len(self.events) + 1)
        self.apply(event)
        store.append(event)
        return event

    def place_order(self, store: EventStore, items: List[dict]) -> Event:
        return self._record(store, "order_placed", {"items": items})

    def receive_payment(self, store: EventStore, amount: float) -> Event:
        return self._record(store, "payment_received", {"amount": amount})

    def cancel(self, store: EventStore, reason: str) -> Event:
        return self._record(store, "order_cancelled", {"reason": reason})

    @classmethod
    def rebuild(cls, order_id: str, events: List[Event]) -> "OrderAggregate":
        order = cls(order_id)
        for event in events:
            order.apply(event)
        return order


if __name__ == "__main__":
    store = EventStore()
    order = OrderAggregate("order-42")

    order.place_order(store, [{"sku": "KB-87", "qty": 1}])
    order.receive_payment(store, 89.99)
    order.cancel(store, "customer_request")

    # Rebuild state from the stored stream — this is the point of event sourcing.
    replayed = OrderAggregate.rebuild("order-42", store.load("order-42"))
    print(f"status after replay: {replayed.status}")
    print(f"events: {len(store.load('order-42'))}")
    for e in store.load("order-42"):
        print(f"  v{e.version} {e.event_type} {e.payload}")
