"""Tests for DDD aggregate invariants.

Run: pytest test_aggregates.py -v
"""
import pytest
from decimal import Decimal
from python_entities_value_objects import Money, OrderStatus, DomainException, InvalidOperation
from python_aggregate_root import Order, OrderConfirmed


def test_cannot_add_item_to_confirmed_order():
    order = Order("order-1", "customer-1")
    order.add_line("prod-1", 2, Money(Decimal("10"), "USD"))
    order.confirm()
    with pytest.raises(InvalidOperation):
        order.add_line("prod-2", 1, Money(Decimal("5"), "USD"))


def test_cannot_confirm_empty_order():
    order = Order("order-1", "customer-1")
    with pytest.raises(DomainException):
        order.confirm()


def test_max_50_items_per_order():
    order = Order("order-1", "customer-1")
    for i in range(50):
        order.add_line(f"prod-{i}", 1, Money(Decimal("1"), "USD"))
    with pytest.raises(InvalidOperation):
        order.add_line("prod-50", 1, Money(Decimal("1"), "USD"))


def test_quantity_must_be_positive():
    order = Order("order-1", "customer-1")
    with pytest.raises(DomainException):
        order.add_line("prod-1", 0, Money(Decimal("10"), "USD"))
    with pytest.raises(DomainException):
        order.add_line("prod-1", -1, Money(Decimal("10"), "USD"))


def test_order_total_sums_lines():
    order = Order("order-1", "customer-1")
    order.add_line("prod-1", 2, Money(Decimal("10"), "USD"))
    order.add_line("prod-2", 3, Money(Decimal("5"), "USD"))
    assert order.total().amount == Decimal("35")


def test_confirm_changes_status():
    order = Order("order-1", "customer-1")
    order.add_line("prod-1", 1, Money(Decimal("10"), "USD"))
    order.confirm()
    assert order.status == OrderStatus.CONFIRMED


def test_confirm_publishes_event():
    order = Order("order-1", "customer-1")
    order.add_line("prod-1", 1, Money(Decimal("10"), "USD"))
    order.confirm()
    events = order.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], OrderConfirmed)
    assert events[0].order_id == "order-1"


def test_pull_events_clears_queue():
    order = Order("order-1", "customer-1")
    order.add_line("prod-1", 1, Money(Decimal("10"), "USD"))
    order.confirm()
    order.pull_events()
    assert len(order.pull_events()) == 0
