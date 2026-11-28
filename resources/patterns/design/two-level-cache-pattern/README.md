# Two-Level Cache Pattern

Runnable examples for [stackpractices.com/patterns/two-level-cache-pattern/](https://stackpractices.com/patterns/two-level-cache-pattern/).

| File | Shows |
|------|-------|
| `two_level_cache.py` | OrderedDict LRU L1 + Redis L2 + pub/sub invalidation listener |
| `two-level-cache.ts` | Map-based L1 + `redis` client L2, publish on invalidate |
| `TwoLevelCacheManager.java` | Caffeine L1 + Jedis L2, publish on invalidate |

## Run

```bash
python two_level_cache.py          # uses fakeredis if installed, else localhost Redis
npx ts-node two-level-cache.ts     # needs a running Redis
# Java: needs caffeine + jedis + jackson-databind on the classpath
```

Key idea: L1 is per-instance, so writes must broadcast invalidations — `invalidate()` publishes on `cache:invalidate` and each instance subscribes in a background thread.
