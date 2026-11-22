import json

import redis


class TenantCache:
    def __init__(self, redis_url: str = 'redis://localhost:6379'):
        self._redis = redis.from_url(redis_url)

    def _key(self, tenant_id: str, key: str) -> str:
        return f'tenant:{tenant_id}:{key}'

    def get(self, tenant_id: str, key: str):
        raw = self._redis.get(self._key(tenant_id, key))
        if raw:
            return json.loads(raw)
        return None

    def set(self, tenant_id: str, key: str, value, ttl: int = 300):
        self._redis.setex(
            self._key(tenant_id, key),
            ttl,
            json.dumps(value, default=str)
        )

    def delete(self, tenant_id: str, key: str):
        self._redis.delete(self._key(tenant_id, key))

    def invalidate_tenant(self, tenant_id: str):
        # SCAN iterates without blocking; KEYS would freeze Redis
        for key in self._redis.scan_iter(match=f'tenant:{tenant_id}:*', count=100):
            self._redis.delete(key)


cache = TenantCache()

def cached_query(tenant_id: str, cache_key: str, query_fn, ttl: int = 300):
    cached = cache.get(tenant_id, cache_key)
    if cached is not None:
        return cached
    result = query_fn()
    cache.set(tenant_id, cache_key, result, ttl)
    return result
