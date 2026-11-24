# Logging estructurado JSON con structlog — Codigo complementario

Setup ejecutable de structlog que emite lineas JSON a stdout.

## Archivos

| Archivo | Que muestra |
|---|---|
| `structured_logging.py` | `configure()` con la cadena completa de processors (contextvars, level, timestamp, redaccion, timing, exception info, JSONRenderer), un `logging_middleware` estilo FastAPI y un smoke test en `__main__`. |

## Inicio rapido

```bash
pip install -r requirements.txt
python structured_logging.py
# {"event": "processing_order", "request_id": "req-abc-123", "user_id": 42, ...}
# {"event": "user_login", "password": "[REDACTED]", ...}
# {"event": "database_query", "duration_ms": 11.2, ...}
```

## Fuente

- https://stackpractices.com/recipes/python-structured-logging-json/
- https://stackpractices.com/es/recipes/python-structured-logging-json/
