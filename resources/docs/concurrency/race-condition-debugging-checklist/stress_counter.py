"""Brute-force stress test: hammers a non-atomic counter from many threads.

A lost-update race on `counter.value += 1` shows up as a final count below
THREADS * INCREMENTS. Run it a few thousand times — one shortfall is a real
bug, not a flake. Section 2.1 of the checklist.

Usage: python stress_counter.py
"""
import threading

THREADS = 100
INCREMENTS = 1000


class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1  # race: read-modify-write is not atomic


def stress() -> int:
    counter = Counter()
    threads = [
        threading.Thread(
            target=lambda: [counter.increment() for _ in range(INCREMENTS)]
        )
        for _ in range(THREADS)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter.value


if __name__ == "__main__":
    expected = THREADS * INCREMENTS
    for run in range(10):
        got = stress()
        status = "OK" if got == expected else f"LOST {expected - got} updates"
        print(f"run {run + 1}: {got}/{expected} {status}")
