"""Tests for DDD value objects.

Run: pytest test_value_objects.py -v
"""
from decimal import Decimal
from python_entities_value_objects import Money, Address


def test_money_equality_by_value():
    assert Money(Decimal("10"), "USD") == Money(Decimal("10"), "USD")


def test_money_inequality_different_amount():
    assert Money(Decimal("10"), "USD") != Money(Decimal("5"), "USD")


def test_money_inequality_different_currency():
    assert Money(Decimal("10"), "USD") != Money(Decimal("10"), "EUR")


def test_money_is_immutable():
    m = Money(Decimal("10"), "USD")
    with pytest.raises(Exception):
        m.amount = Decimal("20")  # type: ignore


def test_money_add_same_currency():
    result = Money(Decimal("10"), "USD").add(Money(Decimal("5"), "USD"))
    assert result == Money(Decimal("15"), "USD")


def test_money_add_different_currency_raises():
    with pytest.raises(ValueError):
        Money(Decimal("10"), "USD").add(Money(Decimal("5"), "EUR"))


def test_money_multiply():
    result = Money(Decimal("10"), "USD").multiply(3)
    assert result == Money(Decimal("30"), "USD")


def test_address_equality_by_value():
    a1 = Address("123 Main St", "NYC", "10001", "US")
    a2 = Address("123 Main St", "NYC", "10001", "US")
    assert a1 == a2


def test_address_inequality():
    a1 = Address("123 Main St", "NYC", "10001", "US")
    a2 = Address("456 Oak Ave", "LA", "90001", "US")
    assert a1 != a2


import pytest
