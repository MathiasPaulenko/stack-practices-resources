# Cache Stampede Prevention Pattern — Runnable Simulations

Companion to the StackPractices pattern [Cache Stampede Prevention Pattern](https://stackpractices.com/patterns/cache-stampede-prevention-pattern/).

A stampede simulator in two languages: 20 concurrent callers hit an expired hot key against an in-memory store that reproduces Redis semantics (`GET`, `SETEX`, `SET NX EX`, check-and-delete release). Stdlib only — no Redis server or dependencies needed.

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/stampede_demo.py` | Python 3.10+ (stdlib only) | `python src/stampede_demo.py` |
| `src/stampede-demo.ts` | Node 20+ / tsx | `npx tsx src/stampede-demo.ts` |

Each run compares a naive cache-aside read (~20 DB queries) against the protected strategies — in-memory single-flight, distributed lock and stale-while-revalidate — printing the DB query count for each. Expected result: the protected strategies collapse the burst to ~1 query.

The `MiniRedis`/`FakeDB` classes are deliberately in-memory so the demo runs anywhere; the coordination code (locks, events, double-check, stale window) mirrors the production implementations in the article.
