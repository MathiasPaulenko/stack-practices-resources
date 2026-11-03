import redis
import time

class RedisRateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def sliding_window(self, key: str, limit: int, window: int) -> bool:
        """Sliding window rate limiter using Redis sorted sets."""
        now = time.time()
        window_start = now - window
        
        pipe = self.redis.pipeline()
        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)
        # Add current request
        pipe.zadd(key, {str(now): now})
        # Count current window
        pipe.zcard(key)
        # Set expiry on key
        pipe.expire(key, window)
        
        results = pipe.execute()
        count = results[2]
        
        return count <= limit

# Usage: 1000 requests per hour per API key
def check_rate_limit(api_key: str, redis_client: redis.Redis) -> bool:
    limiter = RedisRateLimiter(redis_client)
    return limiter.sliding_window(
        key=f"rate_limit:{api_key}",
        limit=1000,
        window=3600
    )
