"""Legacy calculator — the system we want to refactor but can't test directly."""

import json
import sys


def calculate(a, b, operation):
    """Perform a calculation. Has quirks we don't fully understand."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return float("inf") if a > 0 else float("-inf") if a < 0 else float("nan")
        return a / b
    else:
        return None


def main():
    """Read JSON input from stdin, write result to stdout."""
    data = json.load(sys.stdin)
    result = calculate(data["a"], data["b"], data["operation"])
    print(json.dumps({"operation": data["operation"], "a": data["a"], "b": data["b"], "result": result}))


if __name__ == "__main__":
    main()
