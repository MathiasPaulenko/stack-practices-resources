# Thread Pools — Ejemplos ejecutables

Código complementario de https://stackpractices.com/es/recipes/thread-pools/

Cuatro implementaciones del mismo patrón de worker pool:

- `ImageProcessor.java` — pool fijo + `ThreadPoolExecutor` de producción con cola acotada y `CallerRunsPolicy`
- `fetch_urls.py` — `ThreadPoolExecutor` para trabajo I/O-bound, `ProcessPoolExecutor` para CPU-bound (GIL)
- `WorkerPool.cs` — `SemaphoreSlim` + `Task.WhenAll` para concurrencia acotada
- `worker_pool.go` — goroutines + channels + `sync.WaitGroup`

## Ejecutar

- Java: `javac ImageProcessor.java` (necesita un `main` que invoque `productionPool()`)
- Python: `python fetch_urls.py` (necesita `requests`)
- C#: añade `WorkerPool.cs` a un proyecto .NET y llama a `ProcessBatchAsync`
- Go: `go run worker_pool.go`
