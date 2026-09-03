"""Tests for domain events and repository.

Run: pytest test_domain_events.py -v
"""
import pytest
from decimal import Decimal
from python_entities_value_objects import Money
from python_aggregate_root import Order, OrderConfirmed
from python_repositories_events import InMemoryOrderRepository, EventDispatcher


def test_repository_save_and_get():
    repo = InMemoryOrderRepository()
    order = Order("order-1", "customer-1")
    order.add_line("prod-1", 1, Money(Decimal("10"), "USD"))
    repo.save(order)
    retrieved = repo.get("order-1")
    assert retrieved is not None
    assert retrieved.order_id == "order-1"


def test_repository_find_by_customer():
    repo = InMemoryOrderRepository()
    order1 = Order("order-1", "customer-1")
    order2 = Order("order-2", "customer-1")
    order3 = Order("order-3", "customer-2")
    repo.save(order1)
    repo.save(order2)
    repo.save(order3)
    results = repo.find_by_customer("customer-1")
    assert len(results) == 2


def test_event_dispatcher_calls_handlers():
    dispatcher = EventDispatcher()
    received = []
    dispatcher.subscribe(OrderConfirmed, lambda e: received.append(e))

    order = Order("order-1", "customer-1")
    order.add_line("prod-1", 1, Money(Decimal("10"), "USD"))
    order.confirm()
    events = order.pull_events()
    dispatcher.publish(events)

    assert len(received) == 1
    assert isinstance(received[0], OrderConfirmed)


def test_repository_get_nonexistent_returns_none():
    repo = InMemoryOrderRepository()
    assert repo.get("nonexistent") is None
