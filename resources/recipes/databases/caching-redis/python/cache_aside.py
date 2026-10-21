"""Cache-aside helper (redis-py) from the StackPractices Redis caching recipe."""

import json

import redis
from functools import wraps

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def cached(key_prefix, ttl=300):
    """Cache-aside decorator: read-through cache with TTL."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{key_prefix}:{args}:{kwargs}"
            cached_value = r.get(cache_key)
            if cached_value:
                return json.loads(cached_value)
            result = func(*args, **kwargs)
            r.setex(cache_key, ttl, json.dumps(result))
            return result

        return wrapper

    return decorator


@cached("user_profile", ttl=600)
def get_user(user_id):
    """Expensive DB query — here it just returns a stub."""
    return {"id": user_id, "name": "Alice", "orders": 42}


if __name__ == "__main__":
    print(get_user(1))
    print(get_user(1))  # second call served from Redis

    # Manual invalidation
    r.delete("user_profile:(1,):{}")

    # Redis as session store
    r.setex("session:abc123", 3600, json.dumps({"user_id": 1, "role": "admin"}))
