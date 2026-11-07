# Connect to Redis with redis-py: from_url, pool, pipeline, rate limit.
# pip install redis
import os

import redis

# redis://default:password@host:6379/0 — use rediss:// for TLS.
r = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5,
    max_connections=20,
)


def rate_limit(user_id, max_requests=5, window=60):
    key = f"rate:{user_id}"
    current = r.incr(key)
    if current == 1:
        r.expire(key, window)
    return current <= max_requests


if __name__ == "__main__":
    r.set("user:1:name", "Alice", ex=3600)
    print(r.get("user:1:name"))

    r.hset("user:1", mapping={"email": "alice@example.com", "role": "admin"})
    print(r.hgetall("user:1"))

    # Pipeline: batch commands in one round-trip.
    pipe = r.pipeline()
    pipe.set("a", 1)
    pipe.set("b", 2)
    pipe.get("a")
    print(pipe.execute())

    for i in range(7):
        print(f"request {i}:", "allowed" if rate_limit("u42") else "blocked")
