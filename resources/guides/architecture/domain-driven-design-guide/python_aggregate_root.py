"""Aggregate root pattern with invariant enforcement and domain events.

Run: python python_aggregate_root.py
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List
from python_entities_value_objects import (
    Money, OrderLine, OrderStatus, DomainException, InvalidOperation
)


@dataclass
class OrderConfirmed:
    """Domain event: published when an order is confirmed."""
    order_id: str
    customer_id: str
    total: Money
    confirmed_at: datetime = field(default_factory=datetime.now)


class Order:
    """Aggregate root: controls all modifications to Order and OrderLine."""

    def __init__(self, order_id: str, customer_id: str):
        self.order_id = order_id
        self.customer_id = customer_id
        self._lines: List[OrderLine] = []
        self._status = OrderStatus.PENDING
        self._events: List = []

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def lines(self) -> List[OrderLine]:
        return list(self._lines)

    def add_line(self, product_id: str, quantity: int, unit_price: Money):
        """Invariant: cannot modify after confirmation."""
        if self._status != OrderStatus.PENDING:
            raise InvalidOperation("Cannot modify a confirmed order")
        if len(self._lines) >= 50:
            raise InvalidOperation("Max 50 items per order")
        if quantity <= 0:
            raise DomainException("Quantity must be positive")
        self._lines.append(OrderLine(product_id, quantity, unit_price))

    def total(self) -> Money:
        if not self._lines:
            return Money(Decimal("0"), "USD")
        result = self._lines[0].total()
        for line in self._lines[1:]:
            result = result.add(line.total())
        return result

    def confirm(self):
        """Invariant: cannot confirm empty or zero-total order."""
        if not self._lines:
            raise DomainException("Cannot confirm empty order")
        if self.total().amount <= 0:
            raise DomainException("Total must be positive")
        self._status = OrderStatus.CONFIRMED
        self._events.append(OrderConfirmed(
            order_id=self.order_id,
            customer_id=self.customer_id,
            total=self.total(),
        ))

    def pull_events(self) -> List:
        events = self._events
        self._events = []
        return events


def demo():
    order = Order("order-001", "customer-123")
    order.add_line("prod-1", 2, Money(Decimal("15"), "USD"))
    order.add_line("prod-2", 1, Money(Decimal("30"), "USD"))
    print(f"Total: {order.total().amount} {order.total().currency}")

    order.confirm()
    events = order.pull_events()
    print(f"Events published: {len(events)}")
    for e in events:
        print(f"  {type(e).__name__}: order={e.order_id}, total={e.total.amount}")


if __name__ == "__main__":
    demo()
