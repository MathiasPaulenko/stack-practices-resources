# Application-Level Caching — Companion

Runnable caching examples from the [Complete Guide to Application-Level Caching](https://stackpractices.com/guides/complete-guide-application-level-caching/).

## Files

- `lru_cache_decorator.py` — `functools.lru_cache` basics
- `lru_cache_ttl.py` — custom OrderedDict LRU with TTL + RLock
- `lru_cache_node.js` — `lru-cache` package usage
- `caffeine_cache.java` — Caffeine builder with expiry + stats
- `redis_cache.py` — `setex` + JSON serialization pattern
- `memcached_cache.py` — Memcached client with serialized values
- `two_tier_cache.py` — L1 in-memory + L2 Redis hybrid
- `stampede_lock.py` — SET NX EX lock + double-check + bounded retry
- `cache_sizing.py` — footprint estimator
- `threadsafe_cache.py` — RLock-protected dict cache
- `concurrent_map.java` — ConcurrentHashMap + computeIfAbsent
- `node_cache.js` — plain Map cache (single-threaded)
- `cache_warming.py` — startup pre-population
- `resilient_cache.py` — cache-failure fallback
- `monitored_cache.py` — hit/miss counters + hit_rate

- `docker-compose.yaml` — local Redis + Memcached (`docker compose up -d`)

## Usage

Requires `redis`, `python-memcached`, `lru-cache` (npm), Caffeine (Java). Copy the implementation for your tier into your app.

