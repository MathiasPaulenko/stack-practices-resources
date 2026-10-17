# CQRS Pattern — Python demo
# Command side enforces invariants; the read side serves denormalized DTOs.
# In a real system the two sides would live on separate stores and sync via events.

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime


# Write Model (Command Side)
@dataclass
class Order:
    order_id: str
    customer_id: str
    items: List[dict] = field(default_factory=list)
    status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def confirm(self):
        if not self.items:
            raise ValueError("Cannot confirm an empty order")
        self.status = "confirmed"


class OrderCommandHandler:
    """Handles commands — the only way to change state."""

    def __init__(self):
        self.orders: Dict[str, Order] = {}

    def create_order(self, order_id: str, customer_id: str) -> Order:
        order = Order(order_id=order_id, customer_id=customer_id)
        self.orders[order_id] = order
        return order

    def add_item(self, order_id: str, product: str, qty: int, price: float):
        order = self.orders[order_id]
        order.items.append({"product": product, "qty": qty, "price": price})

    def confirm(self, order_id: str):
        self.orders[order_id].confirm()


# Read Model (Query Side) — flat DTO, no behavior
@dataclass
class OrderSummary:
    order_id: str
    customer_id: str
    total: float
    item_count: int
    status: str


class OrderQueryHandler:
    """Serves reads from a denormalized view — never mutates state."""

    def __init__(self, command_store: Dict[str, Order]):
        self.command_store = command_store

    def get_summary(self, order_id: str) -> OrderSummary:
        order = self.command_store[order_id]
        total = sum(i["qty"] * i["price"] for i in order.items)
        return OrderSummary(
            order_id=order.order_id,
            customer_id=order.customer_id,
            total=total,
            item_count=len(order.items),
            status=order.status,
        )

    def list_by_customer(self, customer_id: str) -> List[OrderSummary]:
        return [
            self.get_summary(o.order_id)
            for o in self.command_store.values()
            if o.customer_id == customer_id
        ]


if __name__ == "__main__":
    commands = OrderCommandHandler()
    commands.create_order("ORD-1", "CUST-1")
    commands.add_item("ORD-1", "Laptop", 1, 999.99)
    commands.add_item("ORD-1", "Mouse", 2, 29.99)
    commands.confirm("ORD-1")

    queries = OrderQueryHandler(commands.orders)
    summary = queries.get_summary("ORD-1")
    print(f"Order {summary.order_id}: ${summary.total:.2f} ({summary.item_count} items)")
    print(queries.list_by_customer("CUST-1"))
