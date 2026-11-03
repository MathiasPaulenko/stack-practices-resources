import threading

class ThreadSafeCache:
    def __init__(self):
        self._cache = {}
        self._lock = threading.RLock()
    
    def get(self, key):
        with self._lock:
            return self._cache.get(key)
    
    def set(self, key, value):
        with self._lock:
            self._cache[key] = value
