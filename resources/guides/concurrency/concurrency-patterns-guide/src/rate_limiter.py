"""Semaphore-bounded concurrency.

A semaphore caps how many tasks run at once. This demo simulates 20
requests against an API that tolerates 5 concurrent calls — in flight
never exceeds the limit no matter how many tasks are queued.

Run: python rate_limiter.py
"""

import asyncio
import time


async def fetch(item: int) -> str:
    """Stand-in for a real HTTP call; sleeps to simulate I/O latency."""
    await asyncio.sleep(0.1)
    return f"result-{item}"


class RateLimitedClient:
    def __init__(self, max_concurrent: int = 5) -> None:
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.in_flight = 0
        self.peak = 0

    async def request(self, item: int) -> str:
        async with self.semaphore:
            self.in_flight += 1
            self.peak = max(self.peak, self.in_flight)
            try:
                return await fetch(item)
            finally:
                self.in_flight -= 1


async def main() -> None:
    client = RateLimitedClient(max_concurrent=5)
    start = time.monotonic()
    results = await asyncio.gather(*[client.request(i) for i in range(20)])
    elapsed = time.monotonic() - start
    print(f"{len(results)} results in {elapsed:.2f}s — peak in flight: {client.peak}")
    assert client.peak <= 5, "semaphore bound violated"


if __name__ == "__main__":
    asyncio.run(main())
