# Concurrency Patterns Guide — Code Examples

Runnable examples for the [Concurrency Patterns Guide](https://stackpractices.com/guides/concurrency-patterns-guide/) on StackPractices.

Each file is self-contained and runs standalone. Python examples are `asyncio`-only (no third-party packages) — they simulate I/O with `asyncio.sleep` so you can swap in real `aiohttp`/DB calls.

## Files

| File | Pattern | How to run |
|------|---------|------------|
| `src/producer_consumer.py` | Bounded queue + sentinel shutdown between multiple producers and consumers | `python src/producer_consumer.py` |
| `src/rate_limiter.py` | Semaphore-bounded concurrency; asserts the in-flight cap | `python src/rate_limiter.py` |
| `src/circuit_breaker.py` | CLOSED/OPEN/HALF_OPEN breaker; rejections don't count as failures | `python src/circuit_breaker.py` |
| `src/order_pipeline.py` | `gather` fan-out + `return_exceptions` isolation + semaphore bound | `python src/order_pipeline.py` |
| `src/producer_consumer.go` | Channels + `WaitGroup`; `close()` replaces the sentinel | `go run src/producer_consumer.go` |
| `src/ConcurrencyBasics.java` | Bounded `ThreadPoolExecutor` + `CallerRunsPolicy` + `ReentrantReadWriteLock` | `javac src/ConcurrencyBasics.java && java -cp src ConcurrencyBasics` |
| `src/fetch_all.mjs` | `Promise.all` vs `allSettled` — fail-fast vs isolated results | `node src/fetch_all.mjs` |
| `src/counter.ex` | `GenServer` actor: isolated state via mailbox messages | `elixir src/counter.ex` |
| `tests/test_concurrency.py` | Invariant tests (bound respected, breaker state machine) via `unittest` | `python tests/test_concurrency.py` |

## What each example demonstrates

- **Backpressure**: the bounded `asyncio.Queue` / Go channel blocks producers instead of buffering unbounded work.
- **Failure isolation**: `return_exceptions=True` / `allSettled` keeps one failed call from cancelling the rest in flight.
- **Circuit breaker state machine**: `OPEN` rejections fail fast without touching the dependency or the failure counter.
- **Graceful shutdown**: per-producer sentinels in Python, `close()` + `WaitGroup` in Go, `shutdown()` + `awaitTermination` in Java.
