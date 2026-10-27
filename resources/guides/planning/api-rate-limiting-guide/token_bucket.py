"""Token bucket rate limiter — bursts up to capacity, steady average rate."""
import time
from threading import Lock


class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity      # Maximum burst size
        self.tokens = capacity        # Current tokens available
        self.refill_rate = refill_rate  # Tokens added per second
        self.last_refill = time.time()
        self.lock = Lock()

    def allow_request(self, tokens: int = 1) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            self.tokens = min(
                self.capacity,
                self.tokens + elapsed * self.refill_rate
            )
            self.last_refill = now
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False


# Example: 10 requests/second with burst of 20
bucket = TokenBucket(capacity=20, refill_rate=10)
