"""Sliding-window-counter rate limiter — the memory-light middle ground.

Instead of storing every timestamp (sliding window log), keep two counters:
the current window's count and the previous window's count, and weight the
previous one by how much of it still overlaps the sliding window.

  estimated = prev_count * (1 - elapsed/window) + curr_count

Accurate enough for production, O(1) memory per key.
"""
import time
from threading import Lock


class SlidingWindowCounter:
    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window = window_seconds
        self.lock = Lock()
        self._reset(now=time.time())

    def _reset(self, now: float) -> None:
        self.curr_window_start = now
        self.curr_count = 0
        self.prev_count = 0

    def allow(self) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.curr_window_start
            if elapsed >= 2 * self.window:
                self._reset(now)
                elapsed = 0
            elif elapsed >= self.window:
                self.prev_count = self.curr_count
                self.curr_count = 0
                self.curr_window_start = now
                elapsed = 0
            overlap = max(0.0, 1.0 - elapsed / self.window)
            estimated = self.prev_count * overlap + self.curr_count
            if estimated < self.limit:
                self.curr_count += 1
                return True
            return False


if __name__ == "__main__":
    limiter = SlidingWindowCounter(limit=100, window_seconds=60)  # 100 req/min
    print(limiter.allow())  # True
