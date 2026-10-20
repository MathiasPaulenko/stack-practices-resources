"""Python module — private-by-convention state.

Run: python counter.py
"""

_count = 0  # Module-private by convention (leading underscore)


def _log(operation):
    print(f"Counter {operation}: {_count}")


def increment():
    global _count
    _count += 1
    _log("incremented")
    return _count


def decrement():
    global _count
    _count -= 1
    _log("decremented")
    return _count


def get_count():
    return _count


if __name__ == "__main__":
    increment()
    increment()
    print(get_count())  # 2
    # _count is technically reachable here — the underscore is a social contract
