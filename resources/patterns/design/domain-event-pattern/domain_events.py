"""Domain Event pattern: immutable event + aggregate + in-memory publisher.

Run: python domain_events.py
"""
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Callable, List
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent:
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    aggregate_id: str = ""
    event_type: str = ""
    payload: dict = field(default_factory=dict)


class EventPublisher:
    _handlers: List[Callable] = []

    @classmethod
    def subscribe(cls, handler: Callable):
        cls._handlers.append(handler)

    @classmethod
    def publish(cls, event: DomainEvent):
        for handler in cls._handlers:
            handler(event)


class Order:
    def __init__(self, customer_id: str):
        self.id = str(uuid4())
        self.customer_id = customer_id
        self.lines = []
        self.status = "pending"
        self._events: List[DomainEvent] = []

    def add_line(self, product_id: str, quantity: int, price: float):
        self.lines.append(
            {"product_id": product_id, "quantity": quantity, "price": price}
        )

    def submit(self):
        if not self.lines:
            raise ValueError("Cannot submit empty order")
        self.status = "submitted"
        self._events.append(
            DomainEvent(
                aggregate_id=self.id,
                event_type="OrderSubmitted",
                payload={
                    "customer_id": self.customer_id,
                    "line_count": len(self.lines),
                },
            )
        )

    def clear_events(self):
        events = list(self._events)
        self._events.clear()
        return events


def send_confirmation_email(event: DomainEvent):
    print(f"  [email] order {event.aggregate_id[:8]} confirmed")


def update_analytics(event: DomainEvent):
    print(f"  [analytics] tracked {event.event_type} ({event.payload})")


if __name__ == "__main__":
    EventPublisher.subscribe(send_confirmation_email)
    EventPublisher.subscribe(update_analytics)

    order = Order("cust-123")
    order.add_line("prod-1", 2, 9.99)
    order.submit()

    for event in order.clear_events():
        EventPublisher.publish(event)
