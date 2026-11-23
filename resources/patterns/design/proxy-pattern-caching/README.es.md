# Proxy de Caché — Recursos Companion

Ejemplos ejecutables de [Patrón Proxy para caché de respuestas de API](https://stackpractices.com/es/patterns/proxy-pattern-caching/) de StackPractices.

Un proxy de caché envuelve un cliente de API tras la misma interfaz y sirve las llamadas repetidas desde un mapa TTL. Estos ejemplos van más allá de la versión de manual: **coalescing de peticiones** (los misses concurrentes comparten una única llamada upstream), **métricas de aciertos/fallos**, **evicción LRU** cuando la caché supera `maxSize` e **invalidación explícita** en escrituras.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `caching_client.py` | `CachedWeatherClient` en Python — dict TTL, coalescing thread-safe de llamadas en vuelo, orden LRU, estadísticas |
| `test_caching_client.py` | Suite pytest: 6 tests de aciertos, coalescing de stampede, invalidación, expiración TTL, evicción LRU y ratio de aciertos |
| `caching-client.js` | El mismo proxy en JavaScript — basado en `Map`, coalescing de promesas mediante un mapa `inflight` |
| `caching-client.test.js` | Suite `node:test`: 6 tests equivalentes a la cobertura de Python |

## Ejecutar

```bash
# Demo + tests en Python
python caching_client.py
python -m pytest test_caching_client.py -v

# Demo + tests en JavaScript
node caching-client.js
node --test caching-client.test.js
```

La demo muestra tres llamadores concurrentes compartiendo una única llamada upstream con una clave fría, un acierto de caché en la llamada repetida y el refetch tras `invalidate()`.
