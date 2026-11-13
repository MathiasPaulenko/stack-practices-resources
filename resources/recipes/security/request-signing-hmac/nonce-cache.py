"""In-memory nonce cache for replay protection — alternative to Redis
SET NX for single-process services. Bounded LRU with per-entry TTL."""
import time
from collections import OrderedDict


class NonceCache:
    """LRU cache that tracks nonces seen inside the timestamp window."""

    def __init__(self, max_size: int = 10000, ttl_seconds: int = 300):
        self._cache: OrderedDict[str, float] = OrderedDict()
        self._max_size = max_size
        self._ttl = ttl_seconds

    def check_and_add(self, nonce: str) -> bool:
        """True if the nonce is new, False on replay."""
        now = time.time()
        expired = [k for k, ts in self._cache.items() if now - ts > self._ttl]
        for k in expired:
            self._cache.pop(k, None)

        if nonce in self._cache:
            return False

        self._cache[nonce] = now
        if len(self._cache) > self._max_size:
            self._cache.popitem(last=False)
        return True


if __name__ == "__main__":
    cache = NonceCache()
    print(cache.check_and_add("nonce-1"))  # True — first time
    print(cache.check_and_add("nonce-1"))  # False — replay blocked
    print(cache.check_and_add("nonce-2"))  # True — different nonce
