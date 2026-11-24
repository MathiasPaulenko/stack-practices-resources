# Cache HTTP Responses with httpx and CacheControl — Companion Files

Runnable examples for the recipe
[Cache HTTP Responses with httpx and CacheControl in Python](https://stackpractices.com/recipes/python-httpx-cache-responses/).

## Files

- `client.py` — file-backend and Redis-backend client factories plus a `CachedHttpClient` wrapper with force-refresh and TTL cap. Includes a `__main__` demo against `httpbin.org/cache/60`.
- `requirements.txt` — `httpx`, `cachecontrol[filecache]`, `redis`.

## Usage

```bash
pip install -r requirements.txt
python client.py
```

The demo hits `https://httpbin.org/cache/60`, an endpoint that replies with `Cache-Control: max-age=60`. The first request fetches from the network; the second prints `from_cache=True`.
