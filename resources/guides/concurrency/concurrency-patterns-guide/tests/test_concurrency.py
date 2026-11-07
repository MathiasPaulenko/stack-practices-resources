"""Invariant tests for the concurrency examples.

Asserts invariants under load (all work completed, bounds respected)
rather than interleavings — runs with plain unittest, no pytest needed.

Run: python -m unittest tests.test_concurrency -v   (from repo root dir)
     or: python tests/test_concurrency.py           (from this folder)
"""

import asyncio
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from circuit_breaker import CircuitBreaker, CircuitBreakerOpen, CircuitState, flaky_service
from rate_limiter import RateLimitedClient


class TestCircuitBreaker(unittest.IsolatedAsyncioTestCase):
    async def test_opens_after_threshold_and_rejects_fast(self):
        breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=60)
        for _ in range(2):
            with self.assertRaises(ConnectionError):
                await breaker.call(flaky_service, succeed=False)
        self.assertIs(breaker.state, CircuitState.OPEN)
        # Rejection must not increment the failure count.
        with self.assertRaises(CircuitBreakerOpen):
            await breaker.call(flaky_service, succeed=True)
        self.assertEqual(breaker.failure_count, 2)

    async def test_recovers_after_timeout(self):
        breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=0.05)
        with self.assertRaises(ConnectionError):
            await breaker.call(flaky_service, succeed=False)
        await asyncio.sleep(0.06)
        result = await breaker.call(flaky_service, succeed=True)
        self.assertEqual(result, "ok")
        self.assertIs(breaker.state, CircuitState.CLOSED)


class TestRateLimiter(unittest.IsolatedAsyncioTestCase):
    async def test_never_exceeds_bound_and_completes_all_work(self):
        client = RateLimitedClient(max_concurrent=5)
        results = await asyncio.gather(*[client.request(i) for i in range(50)])
        self.assertEqual(len(results), 50)
        self.assertLessEqual(client.peak, 5)


if __name__ == "__main__":
    unittest.main()
