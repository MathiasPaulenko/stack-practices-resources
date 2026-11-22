import json
import threading
import time
from typing import Any

from redis import Redis


class MultiLevelCache:
    def __init__(
        self,
        redis_client: Redis,
        l1_maxsize: int = 1000,
        l1_ttl: float = 60.0,
    ):
        self.l2 = redis_client
        self.pubsub = redis_client.pubsub()
        self._l1: dict[str, tuple[Any, float]] = {}
        self._l1_maxsize = l1_maxsize
        self._l1_ttl = l1_ttl
        self._lock = threading.Lock()

    def get(self, key: str) -> Any | None:
        with self._lock:
            entry = self._l1.get(key)
            if entry is not None:
                value, expires_at = entry
                if expires_at > time.monotonic():
                    return value
                del self._l1[key]

        l2_value = self.l2.get(key)
        if l2_value:
            value = json.loads(l2_value)
            with self._lock:
                self._l1[key] = (value, time.monotonic() + self._l1_ttl)
                if len(self._l1) > self._l1_maxsize:
                    oldest = next(iter(self._l1))
                    del self._l1[oldest]
            return value

        return None

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        with self._lock:
            self._l1[key] = (value, time.monotonic() + self._l1_ttl)
        self.l2.setex(key, ttl, json.dumps(value, default=str))

    def invalidate(self, key: str) -> None:
        with self._lock:
            self._l1.pop(key, None)
        self.l2.delete(key)
        self.l2.publish("cache:invalidate", json.dumps({"key": key}))

    def listen_for_invalidations(self) -> None:
        """Run in a daemon thread; drops L1 keys invalidated by other instances."""
        self.pubsub.subscribe("cache:invalidate")
        for message in self.pubsub.listen():
            if message["type"] == "message":
                key = json.loads(message["data"])["key"]
                with self._lock:
                    self._l1.pop(key, None)
