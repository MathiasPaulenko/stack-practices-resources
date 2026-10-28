"""Watch eviction rate and memory usage on a Redis instance."""
import time

try:
    import redis
except ImportError:
    raise SystemExit("pip install redis")


def check_cache_memory(r) -> dict:
    info = r.info()
    used = info["used_memory"]
    max_mem = info.get("maxmemory", 0)
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    return {
        "used_memory_mb": used / 1024 / 1024,
        "max_memory_mb": max_mem / 1024 / 1024,
        "memory_usage_pct": (used / max_mem * 100) if max_mem else 0,
        "evicted_keys": info.get("evicted_keys", 0),
        "hit_rate_pct": hits / max(hits + misses, 1) * 100,
        "policy": info.get("maxmemory_policy", "unknown"),
    }


def monitor(r, interval: int = 60):
    prev = 0
    while True:
        m = check_cache_memory(r)
        rate = (m["evicted_keys"] - prev) / interval
        print("[%s] Memory: %.0f/%.0f MB (%.1f%%) | Evictions: %d (%.1f/s) | Policy: %s"
              % (time.strftime("%H:%M:%S"), m["used_memory_mb"], m["max_memory_mb"],
                 m["memory_usage_pct"], m["evicted_keys"], rate, m["policy"]))
        if rate > 100:
            print("ALERT: High eviction rate — consider increasing maxmemory")
        if m["memory_usage_pct"] > 90:
            print("ALERT: Memory usage above 90%")
        prev = m["evicted_keys"]
        time.sleep(interval)


if __name__ == "__main__":
    r = redis.Redis(host="localhost", port=6379, socket_timeout=2)
    print(check_cache_memory(r))
