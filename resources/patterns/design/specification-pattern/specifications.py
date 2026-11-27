"""Composable Specification Pattern over invoice objects."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Invoice:
    id: int
    amount: float
    due_date: datetime
    paid: bool = False
    customer_tier: str = "standard"


class Specification(ABC):
    """A single business rule expressed as a predicate."""

    @abstractmethod
    def is_satisfied_by(self, candidate: Invoice) -> bool:
        pass

    def __and__(self, other: "Specification") -> "Specification":
        return _And(self, other)

    def __or__(self, other: "Specification") -> "Specification":
        return _Or(self, other)

    def __invert__(self) -> "Specification":
        return _Not(self)


class _And(Specification):
    def __init__(self, left: Specification, right: Specification):
        self._left, self._right = left, right

    def is_satisfied_by(self, candidate: Invoice) -> bool:
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(candidate)


class _Or(Specification):
    def __init__(self, left: Specification, right: Specification):
        self._left, self._right = left, right

    def is_satisfied_by(self, candidate: Invoice) -> bool:
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(candidate)


class _Not(Specification):
    def __init__(self, spec: Specification):
        self._spec = spec

    def is_satisfied_by(self, candidate: Invoice) -> bool:
        return not self._spec.is_satisfied_by(candidate)


class Overdue(Specification):
    def is_satisfied_by(self, invoice: Invoice) -> bool:
        return not invoice.paid and invoice.due_date < datetime.now()


class HighValue(Specification):
    def __init__(self, threshold: float = 1000):
        self._threshold = threshold

    def is_satisfied_by(self, invoice: Invoice) -> bool:
        return invoice.amount >= self._threshold


class VIPCustomer(Specification):
    def is_satisfied_by(self, invoice: Invoice) -> bool:
        return invoice.customer_tier == "vip"


class InvoiceRepository:
    def __init__(self, invoices: list[Invoice]):
        self._invoices = invoices

    def find(self, spec: Specification) -> list[Invoice]:
        return [inv for inv in self._invoices if spec.is_satisfied_by(inv)]


def sample_invoices() -> list[Invoice]:
    now = datetime.now()
    return [
        Invoice(1, 500, now - timedelta(days=10), customer_tier="vip"),
        Invoice(2, 2000, now - timedelta(days=5), paid=True, customer_tier="vip"),
        Invoice(3, 3000, now - timedelta(days=20), customer_tier="standard"),
        Invoice(4, 1500, now - timedelta(days=15), customer_tier="vip"),
    ]


if __name__ == "__main__":
    repo = InvoiceRepository(sample_invoices())
    critical = Overdue() & HighValue(1000) & VIPCustomer()
    for inv in repo.find(critical):
        print(f"Critical invoice: #{inv.id}, ${inv.amount}")
