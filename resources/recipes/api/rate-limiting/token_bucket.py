"""Token bucket rate limiter — in-memory, thread-safe.

Usage:
    bucket = TokenBucket(capacity=10, refill_rate=1)  # 10 burst, 1 req/s sustained
    if bucket.allow():
        handle_request()
"""
import time
from threading import Lock


class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = Lock()

    def allow(self) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False


if __name__ == "__main__":
    bucket = TokenBucket(capacity=10, refill_rate=1)
    print(bucket.allow())  # True
