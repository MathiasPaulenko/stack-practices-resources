# Patrones de Asyncio para Producción

Recursos complementarios de la [Guía de Asyncio en Producción](https://stackpractices.com/es/guides/complete-guide-python-asyncio-production/).

## Contenido

| Archivo | Propósito |
| --- | --- |
| `graceful_shutdown.py` | Apagado por señales: cancela workers, limpieza acotada |
| `token_bucket.py` | Rate limiter token bucket asíncrono |
| `watchdog.py` | Detector de event loop parado (basado en hilo) |
| `http_pool.py` | Pool de conexiones aiohttp con límite por semáforo |
| `health_server.py` | Endpoints /health + /live en un puerto aparte |
| `test_asyncio_patterns.py` | Tests pytest-asyncio: timeouts, cancelación, bucket |

## Uso

```bash
pip install aiohttp pytest pytest-asyncio
pytest test_asyncio_patterns.py -v
python graceful_shutdown.py   # Ctrl-C para ver el apagado limpio
```

Consulta la guía para las explicaciones completas y la tabla de resolución de problemas.
