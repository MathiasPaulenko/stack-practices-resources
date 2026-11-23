"""Parameterized test examples — mirrors the pattern article.

Run: pytest test_parameterized.py -v
"""

import csv
from pathlib import Path

import pytest

from calculator import add, evaluate, format_currency
from validators import validate_email


@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (-1, -1, -2),
    (100, 200, 300),
    (0.1, 0.2, 0.3),
])
def test_add(a, b, expected):
    assert add(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("input, expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
    ("  spaces  ", "  SPACES  "),
    ("CamelCase", "CAMELCASE"),
    ("123abc", "123ABC"),
], ids=[
    "lowercase",
    "word",
    "empty",
    "with_spaces",
    "camelcase",
    "alphanumeric",
])
def test_to_upper(input, expected):
    assert input.upper() == expected


@pytest.mark.parametrize("email, is_valid", [
    ("alice@example.com", True),
    ("bob@x.com", True),
    ("invalid", False),
    ("@example.com", False),
    ("alice@", False),
    ("alice@.com", False),
    ("", False),
    (None, False),
], ids=[
    "valid_standard",
    "valid_short",
    "no_at_symbol",
    "no_local_part",
    "no_domain",
    "dot_domain",
    "empty_string",
    "none_input",
])
def test_validate_email(email, is_valid):
    assert validate_email(email) == is_valid


@pytest.mark.parametrize("expression, expected", [
    ("1 + 2", 3),
    ("10 - 5", 5),
    ("3 * 4", 12),
    ("20 / 4", 5),
    ("2 ** 3", 8),
    ("10 % 3", 1),
])
def test_calculator_operations(expression, expected):
    assert evaluate(expression) == expected


@pytest.mark.parametrize("expression", [
    "1 / 0",
    "10 % 0",
    "abc + 1",
    "",
    None,
])
def test_calculator_invalid_input(expression):
    with pytest.raises((ValueError, TypeError)):
        evaluate(expression)


@pytest.mark.parametrize("currency", ["USD", "EUR", "GBP", "JPY"])
@pytest.mark.parametrize("amount", [0, 100, 1000, 10000])
def test_format_currency(amount, currency):
    result = format_currency(amount, currency)
    assert str(amount if amount < 1000 else f"{amount:,}")[0] in result


def _load_csv_cases():
    path = Path(__file__).with_name("email_cases.csv")
    with path.open(newline="") as f:
        return [(row["email"] or None, row["expected"] == "true")
                for row in csv.DictReader(f)]


@pytest.mark.parametrize("email, expected", _load_csv_cases())
def test_validate_email_from_csv(email, expected):
    assert validate_email(email) == expected
