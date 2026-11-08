"""Decorator Pattern simulation: coffee wrapped by milk, sugar, and whip decorators.

Each decorator adds its own cost and label while delegating the rest of the
call to the wrapped object. The demo builds the same stack in two different
orders to show that order affects both cost and description.
"""

from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        ...

    @abstractmethod
    def description(self) -> str:
        ...


class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 2.0

    def description(self) -> str:
        return "simple coffee"


class CoffeeDecorator(Coffee):
    """Base decorator: holds a Coffee and delegates every call by default."""

    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self) -> float:
        return self._coffee.cost()

    def description(self) -> str:
        return self._coffee.description()


class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 0.5

    def description(self) -> str:
        return super().description() + " + milk"


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 0.25

    def description(self) -> str:
        return super().description() + " + sugar"


class WhipDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 0.75

    def description(self) -> str:
        return super().description() + " + whip"


def show(coffee: Coffee) -> None:
    print(f"{coffee.description()} -> ${coffee.cost():.2f}")


def main() -> None:
    print("== plain component ==")
    show(SimpleCoffee())

    print("\n== stacked decorators (milk -> sugar -> whip) ==")
    drink = WhipDecorator(SugarDecorator(MilkDecorator(SimpleCoffee())))
    show(drink)

    print("\n== same decorators, different order (whip -> milk -> sugar) ==")
    drink2 = SugarDecorator(MilkDecorator(WhipDecorator(SimpleCoffee())))
    show(drink2)

    print("\n== decorators compose freely: double milk, no whip ==")
    drink3 = MilkDecorator(MilkDecorator(SimpleCoffee()))
    show(drink3)


if __name__ == "__main__":
    main()
