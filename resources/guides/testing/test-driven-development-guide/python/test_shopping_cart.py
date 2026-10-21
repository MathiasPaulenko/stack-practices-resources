"""Test suite driven by the guide's TDD cycles — one test per red-green loop."""

from shopping_cart import Item, ShoppingCart


def test_empty_cart_total_is_zero():
    cart = ShoppingCart()
    assert cart.total() == 0


def test_add_item_increases_total():
    cart = ShoppingCart()
    cart.add(Item("apple", 1.50))
    assert cart.total() == 1.50


def test_apply_discount():
    cart = ShoppingCart()
    cart.add(Item("laptop", 1000))
    cart.apply_discount("SAVE10")
    assert cart.total() == 900


def test_invalid_discount_code_is_ignored():
    cart = ShoppingCart()
    cart.add(Item("mouse", 25))
    cart.apply_discount("NOTACODE")
    assert cart.total() == 25


def test_total_includes_each_item_once():
    cart = ShoppingCart()
    cart.add(Item("apple", 1.50))
    cart.add(Item("apple", 1.50))
    assert cart.total() == 3.00
