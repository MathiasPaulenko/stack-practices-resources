# test_pricing.py — pytest
# Run: python -m pytest test_pricing.py -v
import pytest
from pricing import parse_price, apply_discount


class TestParsePrice:
    def test_parses_valid_decimal(self):
        assert parse_price('19.99') == 19.99

    def test_rejects_non_numeric(self):
        with pytest.raises(ValueError, match='Invalid price'):
            parse_price('abc')


class TestApplyDiscount:
    def test_applies_percentage(self):
        assert apply_discount(100, 0.1) == pytest.approx(90)

    def test_never_negative(self):
        assert apply_discount(50, 1.5) == 0
