"""Caching proxy — wraps a "remote" client behind the same interface and
serves repeat calls from a TTL cache. Includes request coalescing
(threads waiting on one in-flight call), hit/miss metrics, LRU bounds,
and explicit invalidation.

Run the demo:   python caching_client.py
Run the tests:  python -m pytest test_caching_client.py -v
"""

import threading
import time


class WeatherClient:
    """Real subject stand-in: counts calls like a metered API."""

    def __init__(self):
        self.calls = 0

    def get_forecast(self, city: str) -> dict:
        self.calls += 1
        return {"city": city, "temp": 12 + self.calls, "calls": self.calls}


class CachedWeatherClient:
    """Caching proxy: same interface, TTL dict, in-flight coalescing."""

    def __init__(self, client, ttl_ms: float = 300_000, max_size: int = 1000):
        self.client = client
        self.ttl_ms = ttl_ms
        self.max_size = max_size
        self.cache: dict[str, dict] = {}
        self._access_order: list[str] = []
        self._inflight: dict[str, threading.Event] = {}
        self._lock = threading.Lock()
        self.hits = 0
        self.misses = 0

    def get_forecast(self, city: str) -> dict:
        key = city.lower()
        now = time.time() * 1000
        cached = self.cache.get(key)
        if cached and cached["expiry"] > now:
            self.hits += 1
            self._touch(key)
            return cached["data"]

        # Coalesce concurrent misses into one upstream call.
        with self._lock:
            event = self._inflight.get(key)
            if event is None:
                event = threading.Event()
                self._inflight[key] = event
                leader = True
            else:
                leader = False

        if not leader:
            event.wait()
            return self.cache[key]["data"]

        try:
            self.misses += 1
            data = self.client.get_forecast(city)
            self.cache[key] = {"data": data, "expiry": now + self.ttl_ms}
            self._touch(key)
            self._evict_if_needed()
            return data
        finally:
            with self._lock:
                self._inflight.pop(key)
                event.set()

    def invalidate(self, city: str) -> None:
        self.cache.pop(city.lower(), None)

    def get_stats(self) -> dict:
        total = self.hits + self.misses
        return {"hits": self.hits, "misses": self.misses,
                "hit_rate": self.hits / total if total else 0}

    def _touch(self, key: str) -> None:
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)

    def _evict_if_needed(self) -> None:
        while len(self.cache) > self.max_size:
            oldest = self._access_order.pop(0)
            self.cache.pop(oldest, None)


if __name__ == "__main__":
    real = WeatherClient()
    cached = CachedWeatherClient(real, ttl_ms=60_000)

    cached.get_forecast("London")
    cached.get_forecast("LONDON")  # hit
    print("Upstream calls:", real.calls)  # 1
    print("Stats:", cached.get_stats())

    cached.invalidate("london")
    cached.get_forecast("London")  # miss again
    print("Upstream calls after invalidation:", real.calls)  # 2
