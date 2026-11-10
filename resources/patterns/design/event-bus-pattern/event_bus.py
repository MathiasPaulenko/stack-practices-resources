"""Event Bus pattern: thread-safe in-memory pub/sub with unsubscribe.

Run: python event_bus.py
Test: pytest test_event_bus.py
"""
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any, Callable, Dict, List
import threading


@dataclass
class Event:
    type: str
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


class EventBus:
    """Many-to-many bus: subscribers never know publishers and vice versa.

    Handlers run synchronously on the publisher's thread, in subscription
    order. A handler that raises does not stop the remaining subscribers.
    """

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> Callable[[], None]:
        with self._lock:
            self._subscribers.setdefault(event_type, []).append(handler)

        def unsubscribe() -> None:
            with self._lock:
                handlers = self._subscribers.get(event_type, [])
                if handler in handlers:
                    handlers.remove(handler)

        return unsubscribe

    def publish(self, event: Event) -> None:
        # Iterate over a snapshot so handlers may (un)subscribe during dispatch
        with self._lock:
            handlers = list(self._subscribers.get(event.type, []))
        for handler in handlers:
            try:
                handler(event)
            except Exception as exc:  # noqa: BLE001 - isolate subscriber failures
                print(f"[BUS] handler error for {event.type}: {exc}")


if __name__ == "__main__":
    bus = EventBus()
    received: List[str] = []

    bus.subscribe("UserRegistered", lambda e: received.append(f"email:{e.payload['user_id']}"))
    bus.subscribe("UserRegistered", lambda e: received.append(f"analytics:{e.payload['user_id']}"))
    unsub_crm = bus.subscribe("UserRegistered", lambda e: received.append(f"crm:{e.payload['user_id']}"))

    bus.publish(Event("UserRegistered", {"user_id": 42, "email": "alice@example.com"}))
    print("after first publish:", received)

    unsub_crm()
    bus.publish(Event("UserRegistered", {"user_id": 43, "email": "bob@example.com"}))
    print("after unsubscribe:", received[2:])  # crm must not appear
