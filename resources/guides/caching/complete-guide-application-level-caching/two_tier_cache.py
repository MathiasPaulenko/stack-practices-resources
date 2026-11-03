import redis
import json
import time
from collections import OrderedDict
import threading

class TwoTierCache:
    def __init__(self, redis_client, l1_maxsize: int = 1024, l1_ttl: int = 60, l2_ttl: int = 3600):
        self.redis = redis_client
        self.l1_ttl = l1_ttl
        self.l2_ttl = l2_ttl
        self._l1: OrderedDict = OrderedDict()
        self._l1_maxsize = l1_maxsize
        self._lock = threading.RLock()
    
    def get(self, key: str) -> object | None:
        # L1: in-memory
        with self._lock:
            if key in self._l1:
                value, expires_at = self._l1[key]
                if time.time() <= expires_at:
                    self._l1.move_to_end(key)
                    return value
                else:
                    del self._l1[key]
        
        # L2: Redis
        cached = self.redis.get(key)
        if cached:
            value = json.loads(cached)
            self._set_l1(key, value)
            return value
        
        return None
    
    def set(self, key: str, value: object) -> None:
        self._set_l1(key, value)
        self.redis.setex(key, self.l2_ttl, json.dumps(value))
    
    def _set_l1(self, key: str, value: object) -> None:
        with self._lock:
            if key in self._l1:
                self._l1.move_to_end(key)
            self._l1[key] = (value, time.time() + self.l1_ttl)
            if len(self._l1) > self._l1_maxsize:
                self._l1.popitem(last=False)
    
    def delete(self, key: str) -> None:
        with self._lock:
            self._l1.pop(key, None)
        self.redis.delete(key)

cache = TwoTierCache(r, l1_maxsize=1024, l1_ttl=60, l2_ttl=3600)
