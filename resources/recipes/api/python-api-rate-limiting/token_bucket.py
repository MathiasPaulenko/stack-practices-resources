"""Token bucket rate limiter (in-memory) — companion to the StackPractices recipe.

A bucket holds up to `capacity` tokens and refills at `refill_rate` tokens per
second. Each allowed request consumes one token. Single-process only — use the
Redis Lua variant from the recipe for multi-instance deployments.
"""
import time
from typing import Callable


class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float, clock: Callable[[], float] = time.monotonic):
        if capacity <= 0 or refill_rate <= 0:
            raise ValueError("capacity and refill_rate must be positive")
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self._clock = clock
        self.last_refill = clock()

    def _refill(self) -> None:
        now = self._clock()
        self.tokens = min(self.capacity, self.tokens + (now - self.last_refill) * self.refill_rate)
        self.last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        """Spend `tokens` if the balance covers them."""
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def retry_after(self) -> float:
        """Seconds until at least one token is available."""
        self._refill()
        if self.tokens >= 1:
            return 0.0
        return (1 - self.tokens) / self.refill_rate


def demo() -> None:
    bucket = TokenBucket(capacity=10, refill_rate=1.0)
    results = [bucket.consume() for _ in range(15)]
    allowed = sum(results)
    print(f"burst: {allowed} allowed, {15 - allowed} rejected")
    print(f"retry_after: {bucket.retry_after():.2f}s")


if __name__ == "__main__":
    demo()
