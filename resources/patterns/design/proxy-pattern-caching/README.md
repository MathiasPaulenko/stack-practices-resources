# Caching Proxy — Companion Resources

Runnable examples for [Proxy Pattern for API Response Caching](https://stackpractices.com/patterns/proxy-pattern-caching/) on StackPractices.

A caching proxy wraps an API client behind the same interface and serves repeat calls from a TTL map. These examples go past the textbook version: **request coalescing** (concurrent misses share one upstream call), **hit/miss metrics**, **LRU eviction** when the cache exceeds `maxSize`, and **explicit invalidation** on writes.

## Files

| File | What it shows |
|------|---------------|
| `caching_client.py` | `CachedWeatherClient` in Python — TTL dict, thread-safe in-flight coalescing, LRU order, stats |
| `test_caching_client.py` | pytest suite: 6 tests covering cache hits, stampede coalescing, invalidation, TTL expiry, LRU eviction, hit rate |
| `caching-client.js` | The same proxy in JavaScript — `Map`-based, promise coalescing via an `inflight` map |
| `caching-client.test.js` | `node:test` suite: 6 tests mirroring the Python coverage |

## Run it

```bash
# Python demo + tests
python caching_client.py
python -m pytest test_caching_client.py -v

# JavaScript demo + tests
node caching-client.js
node --test caching-client.test.js
```

The demo shows three concurrent callers sharing one upstream call on a cold key, a cache hit on the repeat call, and refetch after `invalidate()`.
