"""Aggregate root with domain events.

All state changes go through `Order` methods, so invariants live in one
place. Events are collected on the aggregate and published by the caller
*after* the transaction commits.
"""
from dataclasses import dataclass
from datetime import datetime, UTC
from typing import List
from uuid import UUID, uuid4


class DomainEvent:
    pass


@dataclass
class OrderItem:
    product_id: UUID
    quantity: int
    unit_price: float

    def total(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class OrderPlaced(DomainEvent):
    order_id: UUID
    customer_id: UUID
    total: float
    occurred_at: datetime


class Order:
    def __init__(self, customer_id: UUID):
        self.id = uuid4()
        self.customer_id = customer_id
        self.items: List[OrderItem] = []
        self.status = "pending"
        self.domain_events: List[DomainEvent] = []

    def add_item(self, product_id: UUID, quantity: int, unit_price: float):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.status != "pending":
            raise ValueError("Can't modify a submitted order")
        self.items.append(OrderItem(product_id, quantity, unit_price))

    def submit(self):
        if not self.items:
            raise ValueError("Can't submit an empty order")
        if self.status != "pending":
            raise ValueError("Order already submitted")

        self.status = "submitted"
        total = sum(item.total() for item in self.items)
        self.domain_events.append(
            OrderPlaced(
                order_id=self.id,
                customer_id=self.customer_id,
                total=total,
                occurred_at=datetime.now(UTC),
            )
        )

    def cancel(self):
        if self.status == "shipped":
            raise ValueError("Can't cancel a shipped order")
        self.status = "cancelled"

    def clear_events(self):
        self.domain_events.clear()


if __name__ == "__main__":
    order = Order(customer_id=uuid4())
    order.add_item(product_id=uuid4(), quantity=2, unit_price=50.0)
    order.submit()
    for event in order.domain_events:
        print(f"{type(event).__name__}: total={event.total}")
