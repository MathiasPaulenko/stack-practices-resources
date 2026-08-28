"""asyncio.Semaphore patterns for rate limiting and bounded concurrency.

This module collects the seven patterns from the StackPractices recipe:
  1. Basic Semaphore
  2. Rate Limiting API Calls
  3. Token Bucket Rate Limiter
  4. Per-Host Rate Limiting
  5. Database Connection Pool with Semaphore
  6. Dynamic Concurrency Adjustment
  7. Combining Semaphore with Timeout

Run any pattern with ``python semaphore_examples.py <pattern-number>``.
"""

import argparse
import asyncio
import time
from collections import defaultdict
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# 1. Basic Semaphore
# ---------------------------------------------------------------------------
async def basic_semaphore() -> None:
    async def worker(semaphore: asyncio.Semaphore, worker_id: int) -> None:
        async with semaphore:
            print(f"Worker {worker_id} started")
            await asyncio.sleep(1)
            print(f"Worker {worker_id} finished")

    semaphore = asyncio.Semaphore(3)
    tasks = [asyncio.create_task(worker(semaphore, i)) for i in range(10)]
    await asyncio.gather(*tasks)


# ---------------------------------------------------------------------------
# 2. Rate Limiting API Calls (simulated)
# ---------------------------------------------------------------------------
async def rate_limited_api() -> None:
    class RateLimitedClient:
        def __init__(self, max_concurrent: int = 10):
            self.semaphore = asyncio.Semaphore(max_concurrent)

        async def fetch(self, url: str) -> dict:
            async with self.semaphore:
                await asyncio.sleep(0.05)  # simulate network
                return {"url": url, "status": 200}

    client = RateLimitedClient(max_concurrent=5)
    urls = [f"https://api.example.com/data/{i}" for i in range(20)]
    tasks = [client.fetch(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"Fetched {len(results)} URLs with max 5 concurrent")


# ---------------------------------------------------------------------------
# 3. Token Bucket Rate Limiter
# ---------------------------------------------------------------------------
async def token_bucket() -> None:
    class TokenBucketRateLimiter:
        def __init__(self, rate: float, capacity: int):
            self.rate = rate
            self.capacity = capacity
            self.tokens = capacity
            self.last_refill = time.monotonic()
            self.lock = asyncio.Lock()

        async def acquire(self) -> None:
            async with self.lock:
                now = time.monotonic()
                elapsed = now - self.last_refill
                self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
                self.last_refill = now
                if self.tokens < 1:
                    wait_time = (1 - self.tokens) / self.rate
                    await asyncio.sleep(wait_time)
                    self.tokens = 0
                else:
                    self.tokens -= 1

    limiter = TokenBucketRateLimiter(rate=5.0, capacity=10)

    async def rate_limited_fetch(url: str) -> dict:
        await limiter.acquire()
        return {"url": url, "fetched_at": time.monotonic()}

    urls = [f"https://api.example.com/data/{i}" for i in range(10)]
    tasks = [rate_limited_fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(f"Token bucket: fetched {len(results)} URLs at 5/sec")


# ---------------------------------------------------------------------------
# 4. Per-Host Rate Limiting
# ---------------------------------------------------------------------------
async def per_host_rate_limiting() -> None:
    class PerHostRateLimiter:
        def __init__(self, max_per_host: int = 5):
            self.max_per_host = max_per_host
            self.semaphores: dict[str, asyncio.Semaphore] = defaultdict(
                lambda: asyncio.Semaphore(max_per_host)
            )

        def get_semaphore(self, url: str) -> asyncio.Semaphore:
            host = urlparse(url).netloc
            return self.semaphores[host]

        async def fetch(self, url: str) -> dict:
            semaphore = self.get_semaphore(url)
            async with semaphore:
                await asyncio.sleep(0.05)
                return {"url": url, "host": urlparse(url).netloc}

    limiter = PerHostRateLimiter(max_per_host=2)
    urls = [
        "https://api1.example.com/data",
        "https://api1.example.com/data2",
        "https://api1.example.com/data3",
        "https://api2.example.com/data",
        "https://api2.example.com/data2",
    ]
    tasks = [limiter.fetch(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"Per-host: fetched {len(results)} URLs with max 2 per host")


# ---------------------------------------------------------------------------
# 5. Database Connection Pool (simulated)
# ---------------------------------------------------------------------------
async def database_pool() -> None:
    class SimulatedDBPool:
        def __init__(self, max_size: int = 20):
            self.semaphore = asyncio.Semaphore(max_size)
            self.active = 0

        async def query(self, sql: str, *args) -> list:
            async with self.semaphore:
                self.active += 1
                await asyncio.sleep(0.02)
                self.active -= 1
                return [{"sql": sql, "args": args}]

    db = SimulatedDBPool(max_size=10)
    queries = [db.query("SELECT * FROM users WHERE id = $1", i) for i in range(30)]
    results = await asyncio.gather(*queries, return_exceptions=True)
    print(f"DB pool: executed {len(results)} queries with max 10 concurrent")


# ---------------------------------------------------------------------------
# 6. Dynamic Concurrency Adjustment
# ---------------------------------------------------------------------------
async def adaptive_semaphore() -> None:
    class AdaptiveSemaphore:
        def __init__(self, initial: int = 10, min_val: int = 1, max_val: int = 50):
            self._limit = initial
            self.min_val = min_val
            self.max_val = max_val
            self._semaphore = asyncio.Semaphore(initial)
            self._successes = 0
            self._failures = 0
            self._lock = asyncio.Lock()

        async def acquire(self) -> None:
            await self._semaphore.acquire()

        def release(self) -> None:
            self._semaphore.release()

        async def record_success(self) -> None:
            async with self._lock:
                self._successes += 1
                if self._successes >= 10 and self._limit < self.max_val:
                    self._limit += 1
                    self._semaphore.release()
                    self._successes = 0
                    print(f"Increased concurrency to {self._limit}")

        async def record_failure(self) -> None:
            async with self._lock:
                self._failures += 1
                if self._failures >= 3 and self._limit > self.min_val:
                    self._limit -= 1
                    await self._semaphore.acquire()
                    self._failures = 0
                    print(f"Decreased concurrency to {self._limit}")

        @property
        def current_limit(self) -> int:
            return self._limit

    adaptive = AdaptiveSemaphore(initial=5, max_val=20)
    for _ in range(15):
        await adaptive.record_success()
    print(f"Adaptive: final limit = {adaptive.current_limit}")


# ---------------------------------------------------------------------------
# 7. Combining Semaphore with Timeout
# ---------------------------------------------------------------------------
async def semaphore_with_timeout() -> None:
    async def fetch_with_limits(
        semaphore: asyncio.Semaphore,
        item_id: int,
        timeout: float = 0.1,
    ) -> dict:
        async with semaphore:
            try:
                async with asyncio.timeout(timeout):
                    await asyncio.sleep(0.05 if item_id % 3 != 0 else 0.2)
                    return {"id": item_id, "status": "ok"}
            except asyncio.TimeoutError:
                return {"id": item_id, "error": "timeout"}

    semaphore = asyncio.Semaphore(5)
    tasks = [fetch_with_limits(semaphore, i) for i in range(10)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    ok = sum(1 for r in results if isinstance(r, dict) and r.get("status") == "ok")
    print(f"Timeout: {ok}/10 succeeded, rest timed out")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
PATTERNS = {
    1: ("Basic Semaphore", basic_semaphore),
    2: ("Rate Limiting API Calls", rate_limited_api),
    3: ("Token Bucket Rate Limiter", token_bucket),
    4: ("Per-Host Rate Limiting", per_host_rate_limiting),
    5: ("Database Connection Pool", database_pool),
    6: ("Dynamic Concurrency Adjustment", adaptive_semaphore),
    7: ("Combining Semaphore with Timeout", semaphore_with_timeout),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "pattern",
        type=int,
        choices=sorted(PATTERNS.keys()),
        help="Pattern number to run (1-7)",
    )
    args = parser.parse_args()
    name, func = PATTERNS[args.pattern]
    print(f"\n=== Pattern {args.pattern}: {name} ===\n")
    asyncio.run(func())


if __name__ == "__main__":
    main()
