"""Deterministic reproduction: a barrier forces two threads to start at once.

Turns "happens sometimes" into "happens on the first run". Loop it in CI and
count any miss as a real bug. Section 2.2 of the checklist.

Usage: python barrier_repro.py
"""
import threading


def reproduce_once() -> bool:
    """Return True if the reader missed the write (race triggered)."""
    shared = {}
    barrier = threading.Barrier(2)
    result = []

    def writer():
        barrier.wait()  # both threads start at the same time
        shared["key"] = "value"

    def reader():
        barrier.wait()
        result.append(shared.get("key"))  # may not see the write

    t1 = threading.Thread(target=writer)
    t2 = threading.Thread(target=reader)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return result[0] is None


if __name__ == "__main__":
    runs = 1000
    misses = sum(reproduce_once() for _ in range(runs))
    print(f"reader missed the write in {misses}/{runs} runs")
