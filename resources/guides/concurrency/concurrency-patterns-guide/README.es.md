# Guía de Patrones de Concurrencia — Ejemplos de Código

Ejemplos ejecutables de la [Guía de Patrones de Concurrencia](https://stackpractices.com/es/guides/concurrency-patterns-guide/) en StackPractices.

Cada archivo es autocontenido y corre de forma independiente. Los ejemplos Python solo usan `asyncio` (sin paquetes externos) — simulan la I/O con `asyncio.sleep` para que puedas reemplazarlas por llamadas reales con `aiohttp` o a la base de datos.

## Archivos

| Archivo | Patrón | Cómo ejecutarlo |
|---------|--------|-----------------|
| `src/producer_consumer.py` | Cola acotada + apagado por centinela entre varios productores y consumidores | `python src/producer_consumer.py` |
| `src/rate_limiter.py` | Concurrencia acotada por semáforo; afirma el tope en vuelo | `python src/rate_limiter.py` |
| `src/circuit_breaker.py` | Breaker CLOSED/OPEN/HALF_OPEN; los rechazos no cuentan como fallos | `python src/circuit_breaker.py` |
| `src/order_pipeline.py` | Fan-out con `gather` + aislamiento con `return_exceptions` + semáforo | `python src/order_pipeline.py` |
| `src/producer_consumer.go` | Channels + `WaitGroup`; `close()` reemplaza al centinela | `go run src/producer_consumer.go` |
| `src/ConcurrencyBasics.java` | `ThreadPoolExecutor` acotado + `CallerRunsPolicy` + `ReentrantReadWriteLock` | `javac src/ConcurrencyBasics.java && java -cp src ConcurrencyBasics` |
| `src/fetch_all.mjs` | `Promise.all` vs `allSettled` — fallo rápido vs resultados aislados | `node src/fetch_all.mjs` |
| `src/counter.ex` | Actor `GenServer`: estado aislado vía mensajes del mailbox | `elixir src/counter.ex` |
| `tests/test_concurrency.py` | Tests de invariantes (tope respetado, máquina de estados del breaker) con `unittest` | `python tests/test_concurrency.py` |

## Qué demuestra cada ejemplo

- **Backpressure**: la `asyncio.Queue` acotada / el channel de Go frena a los productores en lugar de acumular trabajo sin límite.
- **Aislamiento de fallos**: `return_exceptions=True` / `allSettled` evita que una llamada fallida cancele al resto en vuelo.
- **Máquina de estados del circuit breaker**: los rechazos en `OPEN` fallan rápido sin tocar la dependencia ni el contador de fallos.
- **Apagado limpio**: centinelas por productor en Python, `close()` + `WaitGroup` en Go, `shutdown()` + `awaitTermination` en Java.
