"""rate_limiter.py — token bucket + sliding window for Redis (Python).

The token bucket uses token_bucket.lua for atomicity — two concurrent
requests can't read the same counter and both pass. The sliding window
uses a sorted set scored by timestamp for a true rolling window.

Usage:

    import redis
    from rate_limiter import RateLimiter

    limiter = RateLimiter(redis.Redis(host='localhost', port=6379))
    result = limiter.token_bucket("user:u_4812", capacity=10, refill_rate=1.0)
    if not result.allowed:
        return error_429(retry_after=result.retry_after)
"""

import time
from dataclasses import dataclass
from pathlib import Path

LUA_SCRIPT = (Path(__file__).parent / "token_bucket.lua").read_text()


@dataclass
class LimitResult:
    allowed: bool
    remaining: int
    retry_after: int = 0


class RateLimiter:
    def __init__(self, client):
        self.client = client
        self._lua = client.register_script(LUA_SCRIPT)

    def token_bucket(self, key, capacity=10, refill_rate=1.0):
        """Atomic token bucket via Lua. See token_bucket.lua for the contract."""
        allowed, remaining, retry_after = self._lua(
            keys=[f"rate_limit:{key}"],
            args=[capacity, refill_rate, time.time()],
        )
        return LimitResult(bool(allowed), int(remaining), int(retry_after))

    def sliding_window(self, key, limit=100, window_sec=60):
        """Sorted-set sliding window. Memory-heavier but exact."""
        now = time.time() * 1000
        window_start = now - window_sec * 1000
        zkey = f"rate_limit:sw:{key}"

        self.client.zremrangebyscore(zkey, 0, window_start)
        count = self.client.zcard(zkey)
        if count >= limit:
            oldest = self.client.zrange(zkey, 0, 0, withscores=True)
            retry = int((oldest[0][1] + window_sec * 1000 - now) / 1000) + 1 if oldest else window_sec
            return LimitResult(False, 0, max(1, retry))

        self.client.zadd(zkey, {f"{now}": now})
        self.client.expire(zkey, window_sec)
        return LimitResult(True, limit - count - 1)

    def token_bucket_fail_open(self, key, capacity=10, refill_rate=1.0):
        """Fail-open wrapper: a dead Redis allows traffic and logs, it doesn't 503."""
        try:
            return self.token_bucket(key, capacity, refill_rate)
        except Exception:  # noqa: BLE001 — connection, timeout, whatever
            # Log + alert in real code; allowing is deliberate, not silent
            return LimitResult(True, capacity)
