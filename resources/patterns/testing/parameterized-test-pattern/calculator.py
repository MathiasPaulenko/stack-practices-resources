"""Functions under test for the parameterized examples."""


def add(a, b):
    return a + b


def evaluate(expression: str) -> float:
    """Evaluate a simple arithmetic expression like '3 * 4'.

    Raises ValueError for malformed input and division by zero,
    TypeError for non-string input.
    """
    if not isinstance(expression, str):
        raise TypeError("expression must be a string")
    parts = expression.split()
    if len(parts) != 3:
        raise ValueError("expected '<number> <op> <number>'")
    left, op, right = parts
    try:
        a, b = float(left), float(right)
    except ValueError:
        raise ValueError(f"not a number: {left!r} or {right!r}") from None
    ops = {
        "+": a + b,
        "-": a - b,
        "*": a * b,
        "/": a / b if b != 0 else None,
        "**": a ** b,
        "%": a % b if b != 0 else None,
    }
    if op not in ops:
        raise ValueError(f"unsupported operator: {op!r}")
    if ops[op] is None:
        raise ValueError("division by zero")
    return ops[op]


def format_currency(amount, currency):
    symbols = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}
    if currency not in symbols:
        raise ValueError(f"unsupported currency: {currency}")
    return f"{symbols[currency]}{amount:,}"
