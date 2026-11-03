import time
from collections import OrderedDict
import threading

class LRUCache:
    def __init__(self, maxsize: int = 1024, ttl: int = 3600):
        self.maxsize = maxsize
        self.ttl = ttl
        self._cache: OrderedDict = OrderedDict()
        self._lock = threading.RLock()
    
    def get(self, key: str) -> object | None:
        with self._lock:
            if key not in self._cache:
                return None
            
            value, expires_at = self._cache[key]
            if time.time() > expires_at:
                del self._cache[key]
                return None
            
            self._cache.move_to_end(key)
            return value
    
    def set(self, key: str, value: object) -> None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = (value, time.time() + self.ttl)
            
            if len(self._cache) > self.maxsize:
                self._cache.popitem(last=False)
    
    def delete(self, key: str) -> None:
        with self._lock:
            self._cache.pop(key, None)
    
    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

cache = LRUCache(maxsize=1024, ttl=3600)
