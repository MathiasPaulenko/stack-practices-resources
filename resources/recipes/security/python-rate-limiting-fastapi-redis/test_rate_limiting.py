"""Unit tests for rate limiters — uses fakeredis for in-memory Redis."""
import pytest
import time

try:
    import fakeredis
    HAS_FAKEREDIS = True
except ImportError:
    HAS_FAKEREDIS = False

from sliding_window import SlidingWindowRateLimiter
from token_bucket import TokenBucketRateLimiter
from fixed_window import FixedWindowRateLimiter

pytestmark = pytest.mark.skipif(not HAS_FAKEREDIS, reason="fakeredis not installed")


@pytest.fixture
def redis_client():
    return fakeredis.FakeRedis(decode_responses=True)


@pytest.fixture
def sliding_limiter(redis_client):
    return SlidingWindowRateLimiter(redis_client)


@pytest.fixture
def token_limiter(redis_client):
    return TokenBucketRateLimiter(redis_client)


@pytest.fixture
def fixed_limiter(redis_client):
    return FixedWindowRateLimiter(redis_client)


class TestSlidingWindow:
    def test_allows_first_request(self, sliding_limiter):
        allowed, info = sliding_limiter.is_allowed("user:1", 10, 60)
        assert allowed is True
        assert info["limit"] == 10
        assert info["remaining"] == 9

    def test_blocks_after_limit(self, sliding_limiter):
        for _ in range(5):
            sliding_limiter.is_allowed("user:2", 5, 60)
        allowed, info = sliding_limiter.is_allowed("user:2", 5, 60)
        assert allowed is False
        assert info["remaining"] == 0

    def test_different_keys_independent(self, sliding_limiter):
        for _ in range(3):
            sliding_limiter.is_allowed("user:a", 3, 60)
        allowed_a, _ = sliding_limiter.is_allowed("user:a", 3, 60)
        allowed_b, _ = sliding_limiter.is_allowed("user:b", 3, 60)
        assert allowed_a is False
        assert allowed_b is True

    def test_window_expires(self, sliding_limiter, redis_client, monkeypatch):
        t = [1000.0]
        monkeypatch.setattr(time, "time", lambda: t[0])

        for _ in range(5):
            sliding_limiter.is_allowed("user:3", 5, 60)

        t[0] = 1061.0
        allowed, info = sliding_limiter.is_allowed("user:3", 5, 60)
        assert allowed is True
        assert info["remaining"] == 4


class TestTokenBucket:
    def test_allows_burst_up_to_capacity(self, token_limiter):
        for _ in range(10):
            allowed, _ = token_limiter.is_allowed("user:4", 10, 0.1)
        allowed, info = token_limiter.is_allowed("user:4", 10, 0.1)
        assert allowed is False

    def test_refills_over_time(self, token_limiter, monkeypatch):
        t = [2000.0]
        monkeypatch.setattr(time, "time", lambda: t[0])

        for _ in range(5):
            token_limiter.is_allowed("user:5", 5, 1.0)

        t[0] = 2002.0
        allowed, _ = token_limiter.is_allowed("user:5", 5, 1.0)
        assert allowed is True

    def test_different_keys_independent(self, token_limiter):
        for _ in range(3):
            token_limiter.is_allowed("user:c", 3, 0.1)
        allowed_c, _ = token_limiter.is_allowed("user:c", 3, 0.1)
        allowed_d, _ = token_limiter.is_allowed("user:d", 3, 0.1)
        assert allowed_c is False
        assert allowed_d is True


class TestFixedWindow:
    def test_allows_first_request(self, fixed_limiter):
        allowed, info = fixed_limiter.is_allowed("user:6", 10, 60)
        assert allowed is True
        assert info["limit"] == 10

    def test_blocks_after_limit(self, fixed_limiter):
        for _ in range(5):
            fixed_limiter.is_allowed("user:7", 5, 60)
        allowed, info = fixed_limiter.is_allowed("user:7", 5, 60)
        assert allowed is False

    def test_different_keys_independent(self, fixed_limiter):
        for _ in range(3):
            fixed_limiter.is_allowed("user:e", 3, 60)
        allowed_e, _ = fixed_limiter.is_allowed("user:e", 3, 60)
        allowed_f, _ = fixed_limiter.is_allowed("user:f", 3, 60)
        assert allowed_e is False
        assert allowed_f is True
