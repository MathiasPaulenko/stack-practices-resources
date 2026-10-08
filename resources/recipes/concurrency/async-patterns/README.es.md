# Patrones Async — Recursos Companion

Ejemplos ejecutables de la [receta de Patrones Async](https://stackpractices.com/es/recipes/async-patterns/): fan-out concurrente en tres runtimes — promises de Node.js, `asyncio` de Python y `CompletableFuture` de Java.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `dashboard.js` | `Promise.all` vs `Promise.allSettled` con latencia de I/O simulada; muestra agregación fail-fast vs resiliente |
| `fetch_urls.py` | Fan-out con `asyncio.TaskGroup` más un fetcher acotado por semáforo (requiere `aiohttp`) |
| `AsyncOrderService.java` | Pipeline con `CompletableFuture` usando `thenCompose`/`thenCombine`/`exceptionally`; autocontenido, compila tal cual |

## Inicio rápido

```bash
node dashboard.js                      # sin dependencias, latencia simulada
pip install aiohttp && python fetch_urls.py https://example.com https://example.org
javac AsyncOrderService.java && java AsyncOrderService
```

El demo `dashboard.js` hace fallar la llamada de `Promise.all` a propósito para que veas el rejection, y luego muestra cómo `Promise.allSettled` devuelve resultados parciales en su lugar.
