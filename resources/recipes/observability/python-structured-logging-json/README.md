# Structured JSON Logging with structlog — Companion Code

Runnable structlog setup emitting JSON lines to stdout.

## Files

| File | What it shows |
|---|---|
| `structured_logging.py` | `configure()` with the full processor chain (contextvars, level, timestamp, redaction, timing, exception info, JSONRenderer), a FastAPI-style `logging_middleware`, and a smoke test in `__main__`. |

## Quick start

```bash
pip install -r requirements.txt
python structured_logging.py
# {"event": "processing_order", "request_id": "req-abc-123", "user_id": 42, ...}
# {"event": "user_login", "password": "[REDACTED]", ...}
# {"event": "database_query", "duration_ms": 11.2, ...}
```

## Source

- https://stackpractices.com/recipes/python-structured-logging-json/
- https://stackpractices.com/es/recipes/python-structured-logging-json/
