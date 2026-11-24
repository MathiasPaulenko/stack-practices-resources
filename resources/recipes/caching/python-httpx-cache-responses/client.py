"""Cached HTTP client using httpx + CacheControl.

Companion code for https://stackpractices.com/recipes/python-httpx-cache-responses/

Requirements:
    pip install httpx cachecontrol redis

Usage:
    python client.py
"""

import httpx
from cachecontrol import CacheControlAdapter
from cachecontrol.caches.redis_cache import RedisCache


def file_cache_client(cache_dir="/tmp/http_cache") -> httpx.Client:
    """httpx client with a persistent file-based cache."""
    adapter = CacheControlAdapter(cache_dir=cache_dir)
    return httpx.Client(mount={"https://": adapter, "http://": adapter})


def redis_cache_client(host="localhost", port=6379, db=2) -> httpx.Client:
    """httpx client with a shared Redis cache backend."""
    import redis

    adapter = CacheControlAdapter(
        cache=RedisCache(redis.Redis(host=host, port=port, db=db))
    )
    return httpx.Client(mount={"https://": adapter, "http://": adapter})


class CachedHttpClient:
    """Wrapper with force-refresh and a per-client TTL cap."""

    def __init__(self, cache_dir="/tmp/http_cache", default_ttl=300):
        adapter = CacheControlAdapter(cache_dir=cache_dir)
        self.client = httpx.Client(mount={"https://": adapter, "http://": adapter})
        self.default_ttl = default_ttl

    def get(self, url: str, params: dict = None, force_refresh: bool = False) -> dict:
        headers = {}
        if force_refresh:
            headers["Cache-Control"] = "no-cache"
        elif self.default_ttl:
            headers["Cache-Control"] = f"max-age={self.default_ttl}"

        response = self.client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()


if __name__ == "__main__":
    api = CachedHttpClient(cache_dir="/tmp/api_cache", default_ttl=600)

    url = "https://httpbin.org/cache/60"  # endpoint that sends max-age=60

    first = api.get(url)
    second = api.get(url)

    response = api.client.get(url)
    print(f"from_cache={response.from_cache}")
    print(f"payload={second}")
    api.close()
