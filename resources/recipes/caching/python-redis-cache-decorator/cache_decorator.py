"""Redis-backed cache decorator with TTL and per-call invalidation.

Usage:
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)

    @cached(r, ttl=60, prefix="user")
    def get_user(user_id: str) -> dict:
        ...

    get_user.cache_invalidate("123")
"""

import functools
import hashlib
import inspect
import json
import logging
from typing import Callable, TypeVar

from redis import Redis
from redis.asyncio import Redis as AsyncRedis

logger = logging.getLogger(__name__)
T = TypeVar("T")


def cached(
    redis_client: Redis,
    ttl: int = 300,
    prefix: str = "cache",
    skip_args: tuple[str, ...] = (),
) -> Callable:
    """Cache function results in Redis with a TTL.

    Args:
        redis_client: Redis client instance.
        ttl: Time-to-live in seconds.
        prefix: Cache key prefix.
        skip_args: Argument names to exclude from the cache key.

    Returns:
        Decorator that wraps the function with Redis caching.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            key = _make_key(func, args, kwargs, prefix, skip_args)

            try:
                cached_value = redis_client.get(key)
                if cached_value is not None:
                    return json.loads(cached_value)
            except (json.JSONDecodeError, ConnectionError) as e:
                logger.warning("Cache read failed for %s: %s", key, e)

            result = func(*args, **kwargs)

            try:
                redis_client.setex(key, ttl, json.dumps(result, default=str))
            except (TypeError, ConnectionError) as e:
                logger.warning("Cache write failed for %s: %s", key, e)

            return result

        wrapper.cache_invalidate = _make_invalidator(  # type: ignore[attr-defined]
            redis_client, func, prefix, skip_args
        )
        return wrapper

    return decorator


def async_cached(
    redis_client: AsyncRedis,
    ttl: int = 300,
    prefix: str = "cache",
) -> Callable:
    """Async variant of `cached` for coroutine functions."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = _make_key(func, args, kwargs, prefix, ())

            try:
                cached = await redis_client.get(key)
                if cached is not None:
                    return json.loads(cached)
            except Exception as e:
                logger.warning("Async cache read failed: %s", e)

            result = await func(*args, **kwargs)

            try:
                await redis_client.setex(
                    key, ttl, json.dumps(result, default=str)
                )
            except Exception as e:
                logger.warning("Async cache write failed: %s", e)

            return result

        return wrapper

    return decorator


def invalidate_tag(redis_client: Redis, tag: str) -> int:
    """Delete every key tracked under a tag set. Returns entries removed."""
    keys = redis_client.smembers(f"tag:{tag}")
    if keys:
        redis_client.delete(*keys)
        redis_client.delete(f"tag:{tag}")
    return len(keys)


def _make_key(
    func: Callable,
    args: tuple,
    kwargs: dict,
    prefix: str,
    skip_args: tuple[str, ...],
) -> str:
    """Generate a deterministic cache key from function name and arguments."""
    sig = inspect.signature(func)
    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()

    filtered = {
        k: v
        for k, v in bound.arguments.items()
        if k not in skip_args and k != "self"
    }

    arg_hash = hashlib.sha256(
        json.dumps(filtered, sort_keys=True, default=str).encode()
    ).hexdigest()[:16]

    return f"{prefix}:{func.__module__}:{func.__name__}:{arg_hash}"


def _make_invalidator(
    redis_client: Redis,
    func: Callable,
    prefix: str,
    skip_args: tuple[str, ...],
) -> Callable:
    """Create a cache invalidation function for a specific decorated function."""

    def invalidate(*args, **kwargs) -> int:
        key = _make_key(func, args, kwargs, prefix, skip_args)
        return redis_client.delete(key)

    return invalidate


if __name__ == "__main__":
    import time

    import redis

    r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

    calls = {"count": 0}

    @cached(r, ttl=30, prefix="demo")
    def expensive_lookup(item_id: str) -> dict:
        calls["count"] += 1
        return {"id": item_id, "value": f"computed-{item_id}"}

    print(expensive_lookup("42"))
    print(expensive_lookup("42"))
    assert calls["count"] == 1, "second call should be a cache hit"

    expensive_lookup.cache_invalidate("42")
    print(expensive_lookup("42"))
    assert calls["count"] == 2, "call after invalidation should recompute"
    print("OK: cache hit, miss, and invalidation all behave as expected")
