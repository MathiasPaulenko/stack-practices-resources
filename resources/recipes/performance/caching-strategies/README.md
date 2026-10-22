# Caching Strategies — Companion Code

Runnable examples for the recipe [Caching Strategies: Browser, CDN, Redis & Database](https://stackpractices.com/recipes/caching-strategies/).

## Files

| File | Layer | What it shows |
|------|-------|---------------|
| `cache-aside.js` | Application | Redis cache-aside in Node.js (check cache → DB → populate) |
| `stampede-lock.js` | Application | Stampede protection with `SET NX EX`; only one request rebuilds |
| `swr.js` | Application | Stale-while-revalidate on Redis with a stale flag |
| `multi-level-cache.py` | Application | L1 in-process + L2 Redis + L3 database |
| `event-invalidation.py` | Application | Pub/Sub invalidation on writes, no TTL compromise |
| `cache-warming.py` | Application | Async pre-population of hot keys post-deploy |
| `nginx-cache.conf` | Proxy | `proxy_cache` + `proxy_cache_use_stale` + static-asset headers |
| `sw.js` | Browser | Service Worker with cache-first strategy and version cleanup |
| `materialized-view.sql` | Database | Buffer pool tuning, materialized view, hit-ratio check |

## Requirements

- Node.js 18+ with `redis` (`npm install redis`)
- Python 3.9+ with `redis` (`pip install redis`)
- Redis running on `localhost:6379` (e.g. `docker run -p 6379:6379 redis:7`)
- Nginx 1.18+ for `nginx-cache.conf`
- PostgreSQL 12+ for `materialized-view.sql`

## Quick start

```bash
npm install redis
node cache-aside.js      # MISS then HIT
node stampede-lock.js   # 5 concurrent requests, one rebuild
```

```bash
pip install redis
python multi-level-cache.py
python event-invalidation.py
python cache-warming.py
```
