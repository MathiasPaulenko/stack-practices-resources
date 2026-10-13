"""Deadline propagation through a call chain.

Each layer receives the *remaining* budget, not a fixed timeout, so an
outer 5s deadline shrinks to ~2s by the time it reaches the database.
Headroom between levels is what lets callers react to the failure.
"""

import time


class BudgetExceeded(TimeoutError):
    pass


class DeadlineBudget:
    def __init__(self, total_seconds: float):
        self._end = time.monotonic() + total_seconds

    def remaining(self) -> float:
        return max(0.0, self._end - time.monotonic())

    def guard(self, label: str) -> None:
        if self.remaining() <= 0:
            raise BudgetExceeded(f"Deadline exceeded before {label}")


def api_handler(budget: DeadlineBudget) -> str:
    """Outer layer: reserves headroom to react to the inner failure."""
    budget.guard("api handler")
    with _deadline(min(3.0, budget.remaining())):
        return service_call(budget)


def service_call(budget: DeadlineBudget) -> str:
    """Middle layer: passes a shrunken budget down."""
    budget.guard("service call")
    inner = min(2.0, budget.remaining())
    return db_query(inner)


def db_query(timeout: float) -> str:
    """Inner layer: socket-level timeout on the driver itself."""
    return _query(timeout)


# --- demo plumbing -------------------------------------------------------

import contextlib


@contextlib.contextmanager
def _deadline(seconds: float):
    yield


def _query(timeout: float) -> str:
    if timeout < 0.01:
        raise BudgetExceeded("db query timeout")
    return "rows"


if __name__ == "__main__":
    budget = DeadlineBudget(5.0)
    print(api_handler(budget), "| remaining:", f"{budget.remaining():.2f}s")
