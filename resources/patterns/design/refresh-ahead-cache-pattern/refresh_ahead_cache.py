"""Refresh-ahead cache pattern implementation in Python.

Requires: redis>=4.0, Python 3.9+
Usage: python refresh_ahead_cache.py
"""

import json
import threading
import time
from typing import Any, Callable, Optional

import redis


class RefreshAheadCache:
    """Proactively refreshes cache entries before TTL expires."""

    def __init__(
        self,
        redis_client: redis.Redis,
        ttl: int = 3600,
        refresh_threshold: float = 0.8,
        check_interval: int = 10,
    ):
        self.redis = redis_client
        self.ttl = ttl
        self.refresh_threshold = refresh_threshold
        self.check_interval = check_interval
        self._refresh_callbacks: dict[str, dict] = {}
        self._running = True
        self._refresh_thread = threading.Thread(target=self._refresh_loop, daemon=True)
        self._refresh_thread.start()

    def register(self, key: str, loader: Callable[[], Any], ttl: Optional[int] = None) -> None:
        """Register a hot key for proactive refresh."""
        self._refresh_callbacks[key] = {"loader": loader, "ttl": ttl or self.ttl}
        self._refresh_key(key)

    def get(self, key: str) -> Any:
        """Get a value from cache. Falls back to synchronous load if missing."""
        cached = self.redis.get(key)
        if cached is not None:
            return json.loads(cached)
        if key in self._refresh_callbacks:
            return self._refresh_key(key)
        return None

    def _refresh_loop(self) -> None:
        """Background loop that checks and refreshes entries approaching TTL."""
        while self._running:
            time.sleep(self.check_interval)
            for key, config in list(self._refresh_callbacks.items()):
                ttl_remaining = self.redis.ttl(key)
                threshold = config["ttl"] * (1 - self.refresh_threshold)
                if ttl_remaining < 0 or ttl_remaining < threshold:
                    try:
                        self._refresh_key(key)
                    except Exception as e:
                        print(f"Refresh failed for {key}: {e}")

    def _refresh_key(self, key: str) -> Any:
        """Load data from the loader and update the cache."""
        config = self._refresh_callbacks[key]
        value = config["loader"]()
        self.redis.setex(key, config["ttl"], json.dumps(value))
        return value

    def shutdown(self) -> None:
        """Stop the background refresh thread."""
        self._running = False
        self._refresh_thread.join(timeout=10)


if __name__ == "__main__":
    # Example usage
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    cache = RefreshAheadCache(r, ttl=300, refresh_threshold=0.8)

    # Register hot keys
    cache.register(
        "product:featured",
        lambda: [{"id": 1, "name": "Widget"}],
        ttl=300,
    )

    # Reads always hit cache
    products = cache.get("product:featured")
    print(f"Featured products: {products}")

    cache.shutdown()
