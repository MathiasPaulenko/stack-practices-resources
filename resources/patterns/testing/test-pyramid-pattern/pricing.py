"""Pricing domain logic used by the pytest unit test examples."""


def parse_price(raw: str) -> float:
    """Parse a decimal price string, rejecting non-numeric and negative input."""
    try:
        value = float(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(f'Invalid price: {raw}') from exc
    if value < 0:
        raise ValueError(f'Invalid price: {raw}')
    return value


def apply_discount(total: float, rate: float) -> float:
    """Apply a percentage discount, never returning a negative total."""
    return max(0.0, total * (1 - rate))
