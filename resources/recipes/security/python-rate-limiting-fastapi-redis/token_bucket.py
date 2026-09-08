"""Token bucket rate limiter using Redis Lua scripting for atomicity."""
import time
import redis


class TokenBucketRateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def is_allowed(
        self,
        key: str,
        capacity: int,
        refill_rate: float,
    ) -> tuple[bool, dict]:
        """Token bucket algorithm — allows bursts up to capacity.

        Args:
            key: Unique identifier.
            capacity: Maximum tokens in the bucket.
            refill_rate: Tokens added per second.

        Returns:
            Tuple of (allowed, info_dict).
        """
        now = time.time()
        bucket_key = f"token_bucket:{key}"

        lua_script = """
        local key = KEYS[1]
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        local tokens = tonumber(bucket[1]) or capacity
        local last_refill = tonumber(bucket[2]) or now

        local elapsed = math.max(0, now - last_refill)
        tokens = math.min(capacity, tokens + elapsed * refill_rate)

        local allowed = 0
        if tokens >= 1 then
            tokens = tokens - 1
            allowed = 1
        end

        redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
        redis.call('EXPIRE', key, math.ceil(capacity / refill_rate))

        return {allowed, math.floor(tokens)}
        """

        result = self.redis.eval(
            lua_script, 1, bucket_key,
            capacity, refill_rate, now,
        )

        return bool(result[0]), {
            "limit": capacity,
            "remaining": int(result[1]),
        }
