# Complete Guide to Cache Invalidation — Companion Code

Runnable Redis invalidation patterns for the guide
[Complete Guide to Cache Invalidation](https://stackpractices.com/guides/complete-guide-cache-invalidation/)
on StackPractices.

## Files

| File | What it implements |
| --- | --- |
| `ttl_cache.py` | TTL with jitter + per-type TTL config |
| `event_driven.py` | Write-then-delete + pub/sub broadcast to L1s |
| `versioned_keys.py` | Versioned keys with byte-safe `.decode()` |
| `tag_based.py` | Tag indexing + purge-by-tag |
| `multi_tier.py` | L2 + L1 propaga
