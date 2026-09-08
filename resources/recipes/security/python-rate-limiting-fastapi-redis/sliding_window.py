"""Sliding window rate limiter using Redis sorted sets."""
import time
import redis


class SlidingWindowRateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def is_allowed(
        self,
        key: str,
        max_requests: int,
        window_seconds: int,
    ) -> tuple[bool, dict]:
        """Check if a request is allowed using sliding window algorithm.

        Args:
            key: Unique identifier (user_id, IP, etc.).
            max_requests: Maximum requests in the window.
            window_seconds: Window size in seconds.

        Returns:
            Tuple of (allowed, info_dict with remaining, reset_at).
        """
        now = time.time()
        window_start = now - window_seconds

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zcard(key)
        pipe.zadd(key, {str(now): now})
        pipe.expire(key, window_seconds)
        results = pipe.execute()

        current_count = results[1]
        allowed = current_count < max_requests
        remaining = max(0, max_requests - current_count - 1)

        return allowed, {
            "limit": max_requests,
            "remaining": remaining,
            "reset_at": int(now + window_seconds),
        }
