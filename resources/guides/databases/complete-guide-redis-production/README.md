# Redis in Production — Companion Configs

Production configuration files for [Complete Guide to Redis in Production](https://stackpractices.com/guides/complete-guide-redis-production/).

## Files

-  — hardened redis.conf: bind, auth, maxmemory+eviction, AOF+RDB, dangerous commands renamed.
-  — minimal 3-sentinel quorum setup for automatic failover.
-  — health snapshot: memory, hit rate, evictions, replication lag, slow log.
-  — BGSAVE on a replica + copy off the box.

Adjust , , , and hostnames before use.
