# Thread Pools — Runnable Examples

Companion code for https://stackpractices.com/recipes/thread-pools/

Four implementations of the same worker-pool pattern:

- `ImageProcessor.java` — fixed pool + production `ThreadPoolExecutor` with bounded queue and `CallerRunsPolicy`
- `fetch_urls.py` — `ThreadPoolExecutor` for I/O-bound work, `ProcessPoolExecutor` for CPU-bound (GIL)
- `WorkerPool.cs` — `SemaphoreSlim` + `Task.WhenAll` for bounded concurrency
- `worker_pool.go` — goroutines + channels + `sync.WaitGroup`

## Run

- Java: `javac ImageProcessor.java` (requires a `main` to invoke `productionPool()`)
- Python: `python fetch_urls.py` (needs `requests`)
- C#: add `WorkerPool.cs` to a .NET project and call `ProcessBatchAsync`
- Go: `go run worker_pool.go`
