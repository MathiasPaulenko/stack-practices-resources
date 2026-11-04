# Guía Completa de Concurrencia en Go — Assets del ejemplo

Archivos Go de la [Guía Completa de Concurrencia en Go](https://stackpractices.com/es/guides/complete-guide-go-concurrency/).

| Archivo | Muestra |
| --- | --- |
| `worker_pool.go` | Pool fijo + cancelación ctx + WaitGroup |
| `pipeline.go` | Encadenado de stages con select ctx-aware |
| `semaphore.go` | Semáforo vía buffered channel |
| `errgroup_fanout.go` | Fan-out errgroup con cancelación al primer error |
