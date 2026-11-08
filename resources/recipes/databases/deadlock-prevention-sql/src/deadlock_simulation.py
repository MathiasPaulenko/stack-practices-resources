"""Deadlock simulation: unordered vs ordered lock acquisition.

Models two transactions competing for two row locks. With opposite
acquisition order they deadlock (detected via timeout). With sorted
acquisition order both complete. Stdlib only — no database needed.
"""

import random
import threading
import time


class RowLock:
    """Stand-in for a row lock: acquire blocks with timeout."""

    def __init__(self, row_id: str) -> None:
        self.row_id = row_id
        self._lock = threading.Lock()

    def acquire(self, timeout: float) -> bool:
        return self._lock.acquire(timeout=timeout)

    def release(self) -> None:
        self._lock.release()


LOCK_A = RowLock("A")
LOCK_B = RowLock("B")
DEADLOCK_TIMEOUT = 0.5


def transfer_unordered(first: str, second: str, results: list) -> None:
    """Lock in the given order — deadlock when orders disagree."""
    locks = {"A": LOCK_A, "B": LOCK_B}
    got = []
    for row in (first, second):
        if not locks[row].acquire(timeout=DEADLOCK_TIMEOUT):
            results.append(f"deadlock: could not lock {row}")
            for held in reversed(got):
                locks[held].release()
            return
        got.append(row)
        if len(got) == 1:
            time.sleep(0.05)  # let the other txn grab its first lock
    for held in reversed(got):
        locks[held].release()
    results.append(f"ok: {first}->{second}")


def transfer_ordered(first: str, second: str, results: list) -> None:
    """Sort lock order — the circular wait can never form."""
    first, second = sorted([first, second])
    transfer_unordered(first, second, results)


def execute_with_retry(fn, max_retries: int = 3) -> str:
    """Retry a transaction with exponential backoff + jitter."""
    for attempt in range(max_retries):
        result: list = []
        fn(result)
        outcome = result[-1]
        if outcome.startswith("ok"):
            return outcome
        time.sleep(0.05 * (2**attempt) + random.random() * 0.02)
    return "failed: max retries exceeded"


def main() -> None:
    print("=== Unordered lock acquisition ===")
    results: list = []
    t1 = threading.Thread(target=transfer_unordered, args=("A", "B", results))
    t2 = threading.Thread(target=transfer_unordered, args=("B", "A", results))
    t1.start(); t2.start(); t1.join(); t2.join()
    print("\n".join(results))

    print("\n=== Ordered lock acquisition ===")
    results = []
    t1 = threading.Thread(target=transfer_ordered, args=("A", "B", results))
    t2 = threading.Thread(target=transfer_ordered, args=("B", "A", results))
    t1.start(); t2.start(); t1.join(); t2.join()
    print("\n".join(results))

    print("\n=== Retry with jitter ===")
    outcome = execute_with_retry(
        lambda r: transfer_unordered("A", "B", r) if random.random() < 0.5
        else transfer_ordered("A", "B", r)
    )
    print(outcome)


if __name__ == "__main__":
    main()
