"""Refactored calculator — same behavior as legacy, but cleaner code."""

import json
import sys
from typing import Union

Number = Union[int, float]


def _add(a: Number, b: Number) -> Number:
    return a + b


def _subtract(a: Number, b: Number) -> Number:
    return a - b


def _multiply(a: Number, b: Number) -> Number:
    return a * b


def _divide(a: Number, b: Number) -> Number:
    if b == 0:
        if a > 0:
            return float("inf")
        if a < 0:
            return float("-inf")
        return float("nan")
    return a / b


_OPERATIONS = {
    "add": _add,
    "subtract": _subtract,
    "multiply": _multiply,
    "divide": _divide,
}


def calculate(a: Number, b: Number, operation: str) -> Number:
    """Perform a calculation using a dispatch table."""
    func = _OPERATIONS.get(operation)
    if func is None:
        return None
    return func(a, b)


def main() -> None:
    """Read JSON input from stdin, write result to stdout."""
    data = json.load(sys.stdin)
    result = calculate(data["a"], data["b"], data["operation"])
    print(json.dumps({"operation": data["operation"], "a": data["a"], "b": data["b"], "result": result}))


if __name__ == "__main__":
    main()
