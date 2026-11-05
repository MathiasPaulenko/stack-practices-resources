# token_bucket.py — Async token bucket rate limiter.
import asyncio
import time


class AsyncTokenBucket:
    """Allows `rate` acquisitions per second with bursts up to `capacity`."""

    def __init__(self, rate: float, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = asyncio.Lock()

    async def acquire(self) -> bool:
        async with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_refill = now

            if self.tokens >= 1:
                self.tokens -= 1
                return True

            wait_time = (1 - self.tokens) / self.rate
            await asyncio.sleep(wait_time)
            self.tokens = 0
            return True


# Usage: bucket = AsyncTokenBucket(rate=10, capacity=20)  # 10 req/s, burst 20
