"""Repository pattern and domain event handling for DDD.

Run: python python_repositories_events.py
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from python_aggregate_root import Order, OrderConfirmed


class OrderRepository(ABC):
    """Repository interface: acts like an in-memory collection of aggregates."""

    @abstractmethod
    def get(self, order_id: str) -> Optional[Order]:
        ...

    @abstractmethod
    def save(self, order: Order) -> None:
        ...

    @abstractmethod
    def find_by_customer(self, customer_id: str) -> List[Order]:
        ...


class InMemoryOrderRepository(OrderRepository):
    """In-memory implementation for testing."""

    def __init__(self):
        self._orders = {}

    def get(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def find_by_customer(self, customer_id: str) -> List[Order]:
        return [o for o in self._orders.values() if o.customer_id == customer_id]


class EventDispatcher:
    """Simple event dispatcher for domain events."""

    def __init__(self):
        self._handlers = {}

    def subscribe(self, event_type, handler):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, events):
        for event in events:
            handlers = self._handlers.get(type(event), [])
            for handler in handlers:
                handler(event)


class OrderConfirmedHandler:
    """Example event handler: reacts to OrderConfirmed events."""

    def __call__(self, event: OrderConfirmed):
        print(f"[OrderConfirmed] order={event.order_id} customer={event.customer_id} total={event.total.amount}")


def demo():
    repo = InMemoryOrderRepository()
    dispatcher = EventDispatcher()
    dispatcher.subscribe(OrderConfirmed, OrderConfirmedHandler())

    # Create and save an order
    from decimal import Decimal
    from python_entities_value_objects import Money
    order = Order("order-001", "customer-123")
    order.add_line("prod-1", 2, Money(Decimal("15"), "USD"))
    order.confirm()

    # Publish events
    events = order.pull_events()
    dispatcher.publish(events)

    # Save aggregate
    repo.save(order)
    retrieved = repo.get("order-001")
    print(f"Retrieved order: {retrieved.order_id}, status: {retrieved.status.value}")

    # Find by customer
    customer_orders = repo.find_by_customer("customer-123")
    print(f"Customer has {len(customer_orders)} order(s)")


if __name__ == "__main__":
    demo()
