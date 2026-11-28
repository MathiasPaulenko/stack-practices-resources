"""Two-level cache: LRU L1 + Redis L2, with pub/sub L1 invalidation."""
import json
import time
from collections import OrderedDict

import redis

CHANNEL = "cache:invalidate"


class TwoLevelCache:
    def __init__(self, redis_client: redis.Redis, l1_max_size: int = 1000,
                 l1_ttl: float = 60.0, l2_ttl: int = 3600):
        self.redis = redis_client
        self.l1_max_size = l1_max_size
        self.l1_ttl = l1_ttl
        self.l2_ttl = l2_ttl
        self._l1 = OrderedDict()  # key -> (value, expiry_timestamp)

    def get(self, key: str, loader: callable):
        if key in self._l1:
            value, expiry = self._l1[key]
            if time.time() < expiry:
                self._l1.move_to_end(key)
                return value
            del self._l1[key]

        cached = self.redis.get(key)
        if cached is not None:
            value = json.loads(cached)
            self._populate_l1(key, value)
            return value

        value = loader()
        self._populate_l1(key, value)
        self.redis.setex(key, self.l2_ttl, json.dumps(value))
        return value

    def _populate_l1(self, key: str, value):
        if len(self._l1) >= self.l1_max_size:
            self._l1.popitem(last=False)  # Evict LRU
        self._l1[key] = (value, time.time() + self.l1_ttl)

    def invalidate(self, key: str):
        self._l1.pop(key, None)
        self.redis.delete(key)
        self.redis.publish(CHANNEL, key)  # tell every other instance


def listen_invalidations(cache: TwoLevelCache):
    """Run in a background thread on each instance."""
    pubsub = cache.redis.pubsub()
    pubsub.subscribe(CHANNEL)
    for message in pubsub.listen():
        if message["type"] == "message":
            cache._l1.pop(message["data"].decode(), None)


if __name__ == "__main__":
    # Works without Redis for the L1 part; pass fakeredis for full demo.
    try:
        import fakeredis
        client = fakeredis.FakeStrictRedis()
    except ImportError:
        client = redis.Redis(host="localhost", port=6379)

    cache = TwoLevelCache(client)
    calls = {"n": 0}

    def load_user():
        calls["n"] += 1
        return {"id": "u1", "name": "Ada"}

    print(cache.get("user:u1", load_user))  # DB hit
    print(cache.get("user:u1", load_user))  # L1 hit
    print("loader calls:", calls["n"])      # 1
