import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from specifications import (
    HighValue,
    InvoiceRepository,
    Overdue,
    VIPCustomer,
    sample_invoices,
)


def repo():
    return InvoiceRepository(sample_invoices())


def test_overdue_selects_unpaid_past_due():
    result = repo().find(Overdue())
    assert {i.id for i in result} == {1, 3, 4}


def test_high_value_threshold():
    result = repo().find(HighValue(1000))
    assert {i.id for i in result} == {2, 3, 4}


def test_and_composition():
    result = repo().find(Overdue() & HighValue(1000) & VIPCustomer())
    assert {i.id for i in result} == {4}


def test_or_composition():
    result = repo().find(HighValue(2500) | VIPCustomer())
    assert {i.id for i in result} == {1, 2, 3, 4}


def test_not_composition():
    result = repo().find(~VIPCustomer())
    assert {i.id for i in result} == {3}


def test_nested_composition():
    result = repo().find(VIPCustomer() & (Overdue() | ~HighValue(1000)))
    assert {i.id for i in result} == {1, 4}
