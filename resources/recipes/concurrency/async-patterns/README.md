# Async Patterns — Companion Resources

Runnable examples for the [Async Patterns recipe](https://stackpractices.com/recipes/async-patterns/): concurrent fan-out in three runtimes — Node.js promises, Python `asyncio`, and Java `CompletableFuture`.

## Files

| File | Description |
| --- | --- |
| `dashboard.js` | `Promise.all` vs `Promise.allSettled` with simulated I/O latency; shows fail-fast vs resilient aggregation |
| `fetch_urls.py` | `asyncio.TaskGroup` fan-out plus a semaphore-bounded fetcher (requires `aiohttp`) |
| `AsyncOrderService.java` | `CompletableFuture` pipeline with `thenCompose`/`thenCombine`/`exceptionally`; self-contained, compiles as-is |

## Quick start

```bash
node dashboard.js                      # no dependencies, simulated latency
pip install aiohttp && python fetch_urls.py https://example.com https://example.org
javac AsyncOrderService.java && java AsyncOrderService
```

The `dashboard.js` demo makes the `Promise.all` call fail on purpose so you can see the rejection, then shows how `Promise.allSettled` returns partial results instead.
