# Redis in Production — Companion Configs

Production configuration files for [Complete Guide to Redis in Production](https://stackpractices.com/guides/complete-guide-redis-production/).

## Files

- `redis-prod.conf` — hardened redis.conf: bind, auth, maxmemory+eviction, AOF+RDB, dangerous commands renamed.
- `sentinel.conf` — minimal 3-sentinel quorum setup for automatic failover.
- `monitor.sh` — health snapshot: memory, hit rate, evictions, replication lag, slow log.
- `backup.sh` — BGSAVE on a replica + copy off the box.

Adjust `requirepass`, `maxmemory`, `bind`, and hostnames before use.
