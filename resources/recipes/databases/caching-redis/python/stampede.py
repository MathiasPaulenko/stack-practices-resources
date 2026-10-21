"""Cache stampede protection — lease lock + probabilistic early refresh."""

import json
import random
import time

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def get_with_stampede_protection(cache_key: str, fetcher, ttl: int = 300):
    """Prevent cache stampede using a Redis lock."""
    cached_value = r.get(cache_key)
    if cached_value:
        return json.loads(cached_value)

    lock_key = f"lock:{cache_key}"
    acquired = r.set(lock_key, "1", ex=10, nx=True)

    if acquired:
        try:
            result = fetcher()
            r.setex(cache_key, ttl, json.dumps(result))
            return result
        finally:
            r.delete(lock_key)
    else:
        time.sleep(0.1)
        return get_with_stampede_protection(cache_key, fetcher, ttl)


def get_with_early_refresh(
    cache_key: str, fetcher, ttl: int = 300, early_refresh_pct: float = 0.1
):
    """Probabilistic early expiration — rebuilds the entry before TTL expires."""
    cached_value = r.get(cache_key)
    if cached_value:
        ttl_remaining = r.ttl(cache_key)
        if ttl_remaining < ttl * early_refresh_pct and random.random() < 0.1:
            try:
                result = fetcher()
                r.setex(cache_key, ttl, json.dumps(result))
                return result
            except Exception:
                pass  # Serve stale on refresh failure
        return json.loads(cached_value)

    result = fetcher()
    r.setex(cache_key, ttl, json.dumps(result))
    return result


if __name__ == "__main__":
    fetch = lambda: {"expensive": "db result"}
    print(get_with_stampede_protection("demo:stampede", fetch))
    print(get_with_early_refresh("demo:early", fetch))
