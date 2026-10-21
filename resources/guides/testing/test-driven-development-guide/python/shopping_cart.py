"""Shopping cart built with TDD (red-green-refactor).

Final refactored version from the guide's "A Complete Example" section.
Each test in test_shopping_cart.py maps to one TDD cycle.
"""

DISCOUNTS = {"SAVE10": 0.10, "SAVE20": 0.20}


class Item:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class Discount:
    def __init__(self, code: str, percentage: float):
        self.code = code
        self.percentage = percentage

    def apply(self, amount: float) -> float:
        return amount * (1 - self.percentage)


class ShoppingCart:
    def __init__(self):
        self.items: list[Item] = []
        self.discount: Discount | None = None

    def add(self, item: Item) -> None:
        self.items.append(item)

    def apply_discount(self, code: str) -> None:
        self.discount = Discount(code, DISCOUNTS.get(code, 0))

    def total(self) -> float:
        subtotal = sum(item.price for item in self.items)
        if self.discount:
            return self.discount.apply(subtotal)
        return subtotal
