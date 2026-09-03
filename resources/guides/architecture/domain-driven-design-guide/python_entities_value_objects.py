"""DDD building blocks: entities, value objects, and ubiquitous language.

Run: python python_entities_value_objects.py
"""
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import List


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Money:
    """Value object: immutable, compared by attributes."""
    amount: Decimal
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def multiply(self, factor: int) -> "Money":
        return Money(self.amount * factor, self.currency)

    @classmethod
    def ZERO(cls, currency: str = "USD") -> "Money":
        return cls(Decimal("0"), currency)


@dataclass(frozen=True)
class Address:
    """Value object: no identity, defined by attributes."""
    street: str
    city: str
    postal_code: str
    country: str


class OrderLine:
    """Entity within an aggregate (not a root)."""
    def __init__(self, product_id: str, quantity: int, unit_price: Money):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

    def total(self) -> Money:
        return self.unit_price.multiply(self.quantity)


class Order:
    """Entity with identity (order_id)."""

    def __init__(self, order_id: str, customer_id: str):
        self.order_id = order_id
        self.customer_id = customer_id
        self._lines: List[OrderLine] = []
        self._status = OrderStatus.PENDING

    @property
    def status(self) -> OrderStatus:
        return self._status

    def add_line(self, product_id: str, quantity: int, unit_price: Money):
        if self._status != OrderStatus.PENDING:
            raise InvalidOperation("Cannot modify a confirmed order")
        if len(self._lines) >= 50:
            raise InvalidOperation("Max 50 items per order")
        self._lines.append(OrderLine(product_id, quantity, unit_price))

    def total(self) -> Money:
        if not self._lines:
            return Money.ZERO()
        result = self._lines[0].total()
        for line in self._lines[1:]:
            result = result.add(line.total())
        return result

    def confirm(self):
        if not self._lines:
            raise DomainException("Cannot confirm empty order")
        if self.total().amount <= 0:
            raise DomainException("Total must be positive")
        self._status = OrderStatus.CONFIRMED


class DomainException(Exception):
    """Raised when a domain rule is violated."""
    pass


class InvalidOperation(Exception):
    """Raised when an operation is not valid in the current state."""
    pass


def demo():
    # Value objects are interchangeable
    price1 = Money(Decimal("10"), "USD")
    price2 = Money(Decimal("10"), "USD")
    assert price1 == price2, "Value objects with same attributes are equal"

    # Entities have identity
    order = Order("order-001", "customer-123")
    order.add_line("prod-1", 2, Money(Decimal("15"), "USD"))
    order.add_line("prod-2", 1, Money(Decimal("30"), "USD"))
    print(f"Order {order.order_id} total: {order.total().amount} {order.total().currency}")

    order.confirm()
    print(f"Order status: {order.status.value}")

    # Cannot modify confirmed order
    try:
        order.add_line("prod-3", 1, Money(Decimal("5"), "USD"))
    except InvalidOperation as e:
        print(f"Correctly blocked: {e}")


if __name__ == "__main__":
    demo()
