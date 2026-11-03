"""TTL-based cache with jitter to prevent stampedes.

Source: https://stackpractices.com/guides/complete-guide-cache-invalidation/
"""
import json
import random


def set_with_jitter(r, key: str, value: str, base_ttl: int = 3600,
                    jitter_pct: int = 20):
    jitter = int(base_ttl * jitter_pct / 100)
    r.setex(key, base_ttl + random.randint(0, jitter), value)


TTL_CONFIG = {
    "user_profile": 300,
    "product_catalog": 3600,
    "app_config": 86400,
    "search_results": 60,
    "real_time_stats": 0,
}


def get_with_ttl(r, key: str, loader, data_type: str):
    ttl = TTL_CONFIG.get(data_type, 300)
    if ttl == 0:
        return loader()
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    value = loader()
    if value:
        set_with_jitter(r, key, json.dumps(value), base_ttl=ttl)
    return value
