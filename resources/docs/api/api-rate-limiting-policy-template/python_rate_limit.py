"""Token bucket rate limiter backed by Redis."""
import time
import redis


def rate_limit(redis_client, key, capacity, refill_rate, interval_sec):
    bucket_key = f"ratelimit:{key}"
    now = time.time()
    # NOTE: illustrative pipeline — not atomic across instances.
    # In production, run the same logic as a Lua EVAL script on Redis.
    pipe = redis_client.pipeline()
    pipe.hgetall(bucket_key)
    pipe.hset(bucket_key, tokens=capacity, lastRefill=now)
    pipe.expire(bucket_key, interval_sec * 2)
    results = pipe.execute()

    bucket = results[0]
    tokens = float(bucket.get(b"tokens", capacity))
    last_refill = float(bucket.get(b"lastRefill", now))
    elapsed = now - last_refill
    tokens = min(capacity, tokens + elapsed * (capacity / interval_sec))

    if tokens >= 1:
        tokens -= 1
        redis_client.hset(bucket_key, tokens=tokens, lastRefill=now)
        return {"allowed": True, "remaining": int(tokens)}
    retry_after = int((1 - tokens) / (capacity / interval_sec)) + 1
    redis_client.hset(bucket_key, tokens=tokens, lastRefill=now)
    return {"allowed": False, "remaining": 0, "retryAfter": retry_after}
