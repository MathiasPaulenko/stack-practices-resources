from dataclasses import dataclass
from datetime import datetime
from typing import List
import uuid


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    quantity: int
    unit_price: float

    def total(self) -> float:
        return self.quantity * self.unit_price


class Order:
    """Aggregate root: external code can only modify the order through its public methods."""

    def __init__(self, customer_id: str):
        self.id = str(uuid.uuid4())
        self.customer_id = customer_id
        self.lines: List[OrderLine] = []
        self.status = "pending"
        self.created_at = datetime.now()
        self.version = 0

    def add_line(self, product_id: str, quantity: int, unit_price: float):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.status != "pending":
            raise ValueError("Can't modify a non-pending order")

        self.lines.append(OrderLine(product_id, quantity, unit_price))
        self.version += 1

    def remove_line(self, product_id: str):
        if self.status != "pending":
            raise ValueError("Can't modify a non-pending order")

        self.lines = [line for line in self.lines if line.product_id != product_id]
        self.version += 1

    def total(self) -> float:
        return sum(line.total() for line in self.lines)

    def submit(self):
        if not self.lines:
            raise ValueError("Can't submit an empty order")
        self.status = "submitted"
        self.version += 1


if __name__ == "__main__":
    order = Order(customer_id="cust-123")
    order.add_line("prod-1", 2, 9.99)
    order.add_line("prod-2", 1, 19.99)
    print(f"Total: {order.total():.2f}")  # 39.97
    order.submit()
    print(f"Order {order.id} status: {order.status}")
