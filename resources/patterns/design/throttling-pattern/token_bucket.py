import time
import threading
from dataclasses import dataclass, field


@dataclass
class TokenBucket:
    capacity: int
    refill_rate: float          # tokens per second
    tokens: float = field(init=False)
    last_refill: float = field(init=False)
    lock: threading.Lock = field(init=False)

    def __post_init__(self):
        self.tokens = float(self.capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self, tokens: int = 1) -> bool:
        with self.lock:
            now = time.monotonic()
            self.tokens = min(
                self.capacity,
                self.tokens + (now - self.last_refill) * self.refill_rate,
            )
            self.last_refill = now
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False


class RateLimitExceeded(Exception):
    pass


class ThrottledAPI:
    def __init__(self):
        # 10 burst capacity, 2 requests/second sustained
        self.bucket = TokenBucket(capacity=10, refill_rate=2)

    def call(self, endpoint: str, data: dict) -> dict:
        if not self.bucket.acquire():
            raise RateLimitExceeded("Rate limit exceeded. Try again later.")
        return {"status": "success", "endpoint": endpoint}
