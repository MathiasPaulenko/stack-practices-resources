"""Cache-aside (lazy loading) with Redis, TTL and stampede protection.

The application checks the cache first; on a miss it loads from the
database, fills the cache with a TTL and returns the value. Writes go to
the database and then delete the cache key (invalidate, not update).

A per-key lock (SET NX PX) makes sure only one concurrent miss hits the
database while the rest wait briefly and retry — the thundering-herd fix.

Requires: pip install redis (use fakeredis to run the demo offline).
"""

import json
import time
from typing import Any, Callable, Optional

import redis


class CacheAside:
    """Redis-backed cache-aside with TTL, invalidation and a fill lock."""

    def __init__(
        self,
        redis_client: redis.Redis,
        ttl_seconds: int = 300,
        lock_ttl_ms: int = 3000,
        wait_ms: int = 50,
        wait_attempts: int = 20,
    ):
        self.redis = redis_client
        self.ttl = ttl_seconds
        self.lock_ttl_ms = lock_ttl_ms
        self.wait_ms = wait_ms
        self.wait_attempts = wait_attempts

    def get(self, key: str, loader: Callable[[], Optional[dict]]) -> Optional[dict]:
        raw = self.redis.get(key)
        if raw is not None:
            return json.loads(raw)

        # Cache miss: only one caller loads, the rest wait and retry.
        lock_key = f"{key}:lock"
        if self.redis.set(lock_key, "1", nx=True, px=self.lock_ttl_ms):
            try:
                value = loader()
                if value is not None:
                    self.redis.setex(key, self.ttl, json.dumps(value))
                return value
            finally:
                self.redis.delete(lock_key)

        # Another request is filling the key — wait and retry the cache.
        for _ in range(self.wait_attempts):
            time.sleep(self.wait_ms / 1000)
            raw = self.redis.get(key)
            if raw is not None:
                return json.loads(raw)
        return loader()  # Lock holder gave up; load directly.

    def set_source(self, key: str, value: dict, db_writer: Callable[[dict], Any]) -> None:
        """Write path: update the database, then invalidate the cache key."""
        db_writer(value)
        self.redis.delete(key)


if __name__ == "__main__":
    try:
        import fakeredis

        client = fakeredis.FakeRedis()
    except ImportError:
        client = redis.Redis()

    store = CacheAside(client, ttl_seconds=60)
    calls = {"count": 0}

    def load_user() -> dict:
        calls["count"] += 1
        return {"id": 1, "name": "User 1"}

    print(store.get("user:1", load_user))  # miss -> DB
    print(store.get("user:1", load_user))  # hit
    print("DB calls:", calls["count"])   # -> 1
