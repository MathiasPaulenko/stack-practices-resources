from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    """Value object shared across modules. Immutable, currency-aware."""

    amount_cents: int
    currency: str = "USD"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount_cents + other.amount_cents, self.currency)
