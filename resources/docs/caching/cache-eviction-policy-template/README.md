# Cache Eviction Policy Template

Companion code for [Cache Eviction Policy Template](https://stackpractices.com/docs/cache-eviction-policy-template/).

## Contents

| File | What it is |
|------|------------|
| `redis-local.conf` | L2 local Redis config: `allkeys-lru`, 4 GB `maxmemory` |
| `redis-cluster.conf` | L3 shared cluster config: `volatile-ttl`, 32 GB |
| `monitor_eviction.py` | Eviction rate + memory monitor with alert thresholds (`evicted_keys`, hit rate, usage %) |

## How to use

- Copy a conf into your Redis deployment and adjust `maxmemory` to your host (max ~75% of RAM).
- `python monitor_eviction.py` — needs `pip install redis` and a reachable instance.
