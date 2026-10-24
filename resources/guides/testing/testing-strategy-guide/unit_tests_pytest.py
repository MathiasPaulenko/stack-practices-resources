"""Unit test examples from the guide's Unit Testing section.

Run: pytest unit_tests_pytest.py -v
"""


def calculate_discount(price: float, customer_type: str) -> float:
    """Return the discounted price for the given customer type."""
    if customer_type == "vip":
        return price * 0.8
    return price * 0.95


import pytest


@pytest.mark.parametrize(
    "price,customer_type,expected",
    [
        (100.0, "vip", 80.0),
        (100.0, "regular", 95.0),
        (0.0, "vip", 0.0),
    ],
)
def test_calculate_discount(price, customer_type, expected):
    """Boundary and business-rule cases in one parametrized test."""
    assert calculate_discount(price, customer_type) == expected
