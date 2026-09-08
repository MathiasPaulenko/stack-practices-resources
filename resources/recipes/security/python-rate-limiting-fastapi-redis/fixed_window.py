"""Fixed window rate limiter — simpler but allows bursts at window boundaries."""
import time
import redis


class FixedWindowRateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def is_allowed(
        self,
        key: str,
        max_requests: int,
        window_seconds: int,
    ) -> tuple[bool, dict]:
        """Fixed window — simpler but allows bursts at window boundary.

        Args:
            key: Unique identifier.
            max_requests: Maximum requests in the window.
            window_seconds: Window size in seconds.

        Returns:
            Tuple of (allowed, info_dict).
        """
        now = int(time.time())
        window = now - (now % window_seconds)
        window_key = f"fixed_window:{key}:{window}"

        pipe = self.redis.pipeline()
        pipe.incr(window_key)
        pipe.expire(window_key, window_seconds)
        results = pipe.execute()

        count = results[0]
        allowed = count <= max_requests
        remaining = max(0, max_requests - count)

        return allowed, {
            "limit": max_requests,
            "remaining": remaining,
            "reset_at": window + window_seconds,
        }
