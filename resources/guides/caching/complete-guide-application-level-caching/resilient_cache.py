class MonitoredCache:
    def __init__(self, cache):
        self.cache = cache
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        value = self.cache.get(key)
        if value is not None:
            self.hits += 1
        else:
            self.misses += 1
        return value
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
