# Proxy Pattern — Companion Resources

Runnable examples for the [Proxy pattern](https://stackpractices.com/patterns/proxy-pattern/) on StackPractices.

A proxy sits in front of a real object behind the same interface and decides what happens to each call: forward it, reject it, cache the result, or defer the real work. These examples compose three single-purpose proxies — virtual (lazy init), caching, and protection — around one `ReportService`, so each layer stays small and the composition does the work.

## Files

| File | What it shows |
|------|---------------|
| `proxy.py` | `LazyReportService`, `CachedReportService` and `ProtectedReportService` in Python wrapping a `ReportService` |
| `test_proxy.py` | pytest suite: 7 tests covering lazy init, memoization stats, per-key caching, invalidation and role checks |
| `proxy.js` | The same three proxies in JavaScript |
| `proxy.test.js` | `node:test` suite: 7 tests mirroring the Python coverage |

## Run it

```bash
# Python demo + tests
python proxy.py
python -m pytest test_proxy.py -v

# JavaScript demo + tests
node proxy.js
node --test proxy.test.js
```

Expected demo output shows the lazy proxy staying uninitialized until the first call, the cache serving a hit on the second `generate()`, and the protection proxy rejecting an unknown role without ever reaching the real subject.
