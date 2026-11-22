# Multi-Level Cache L1+L2 — Companion Files

Runnable code for the recipe [Multi-Level Cache with In-Memory L1 and Redis L2](https://stackpractices.com/recipes/multi-level-cache-l1-l2/).

## Files

- `multi-level-cache.ts` — TypeScript implementation: in-memory L1 (`lru-cache`), Redis L2, pub/sub invalidation across instances.
- `usage.ts` — example wiring: `getOrLoad` plus invalidation after a write.
- `instrumented-cache.ts` — subclass that tracks L1/L2/miss hit rates.
- `multi_level_cache.py` — Python variant (3.10+) with a daemon-thread pub/sub listener.

## Requirements

- Node.js 18+, `npm install redis lru-cache`
- Python 3.10+, `pip install redis`
- A running Redis (`redis://localhost:6379` by default)
