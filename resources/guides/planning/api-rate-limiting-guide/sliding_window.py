"""Sliding window rate limiters — log (exact) and counter (memory-efficient)."""
import time
from collections import deque
from threading import Lock


class SlidingWindowLog:
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size  # Seconds
        self.max_requests = max_requests
        self.requests = deque()
        self.lock = Lock()

    def allow_request(self) -> bool:
        with self.lock:
            now = time.time()
            cutoff = now - self.window_size
            while self.requests and self.requests[0] < cutoff:
                self.requests.popleft()
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False


class SlidingWindowCounter:
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests
        self.current_window = int(time.time() // window_size)
        self.current_count = 0
        self.previous_count = 0
        self.lock = Lock()

    def allow_request(self) -> bool:
        with self.lock:
            now = int(time.time())
            window = now // self.window_size
            if window != self.current_window:
                self.previous_count = self.current_count
                self.current_count = 0
                self.current_window = window
            elapsed = now % self.window_size
            weight = 1 - (elapsed / self.window_size)
            estimated = (self.previous_count * weight) + self.current_count
            if estimated < self.max_requests:
                self.current_count += 1
                return True
            return False
