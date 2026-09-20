"""test_rate_limiter.py — pytest coverage for the four scenarios from the recipe.

Uses fakeredis so the suite runs without a live Redis:
    pip install pytest fakeredis redis
    pytest test_rate_limiter.py -v

Scenarios: enforcement (N+1 rejected), window reset, Redis failover
(fail-open), and distributed consistency (concurrent increments).
"""

import threading
import time

import fakeredis
import pytest

from rate_limiter import RateLimiter


@pytest.fixture()
def limiter():
    return RateLimiter(fakeredis.FakeStrictRedis())


class TestEnforcement:
    def test_nth_plus_one_request_is_rejected(self, limiter):
        for _ in range(10):
            assert limiter.token_bucket("user:u1", capacity=10, refill_rate=1.0).allowed
        result = limiter.token_bucket("user:u1", capacity=10, refill_rate=1.0)
        assert not result.allowed
        assert result.retry_after >= 1

    def test_retry_after_reported_on_rejection(self, limiter):
        for _ in range(5):
            limiter.sliding_window("user:u2", limit=5, window_sec=60)
        result = limiter.sliding_window("user:u2", limit=5, window_sec=60)
        assert not result.allowed
        assert 1 <= result.retry_after <= 60


class TestWindowReset:
    def test_requests_allowed_after_refill(self, limiter):
        """Boundary check: capacity drains, then refills over time."""
        for _ in range(10):
            limiter.token_bucket("user:u3", capacity=10, refill_rate=10.0)
        assert not limiter.token_bucket("user:u3", capacity=10, refill_rate=10.0).allowed
        # 10 tokens/s refill → 1 token back in ~0.1s
        time.sleep(0.15)
        assert limiter.token_bucket("user:u3", capacity=10, refill_rate=10.0).allowed


class TestRedisFailover:
    def test_fail_open_when_redis_is_down(self):
        """A dead Redis allows traffic — the API doesn't 503 on limiter failure."""
        class DeadRedis:
            def register_script(self, script):
                def boom(*args, **kwargs):
                    raise ConnectionError("redis is down")
                return boom

        limiter = RateLimiter(DeadRedis())
        result = limiter.token_bucket_fail_open("user:u4", capacity=10, refill_rate=1.0)
        assert result.allowed


class TestDistributedConsistency:
    def test_concurrent_requests_share_the_limit(self, limiter):
        """20 threads fire at capacity 10 — at most 10 may pass."""
        results = []

        def attempt():
            results.append(limiter.token_bucket("shared:key", capacity=10, refill_rate=0.01).allowed)

        threads = [threading.Thread(target=attempt) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert sum(results) <= 10
        assert len(results) == 20
