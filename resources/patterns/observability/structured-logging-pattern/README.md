# Structured Logging — Companion Resources

Companion code for the [Structured Logging pattern](https://stackpractices.com/patterns/structured-logging-pattern/) on StackPractices.

## Files

| File | Language | Description |
| --- | --- | --- |
| `structlog_example.py` | Python 3.10+ | structlog setup: JSON renderer, bound request context, sensitive-field redaction processor |
| `json_formatter.py` | Python 3.10+ | Zero-dependency `logging.Formatter` that emits one JSON line per record |
| `async_logging.py` | Python 3.10+ | `QueueHandler`/`QueueListener` pair for non-blocking logging on hot paths |
| `logging_pino.js` | Node.js 20+ | pino setup: ISO timestamps, base metadata, child loggers, endpoint sampling |
| `test_structured_logging.py` | Python + pytest | Verifies JSON output shape, redaction, bound context and queue delivery |

## Quick start

### Python (pytest)

```bash
pip install structlog pytest
pytest test_structured_logging.py
```

### Python examples

```bash
python structlog_example.py   # bound context + redaction
python json_formatter.py      # stdlib JSON formatter
python async_logging.py       # queue-based non-blocking logging
```

### Node.js (pino)

```bash
npm install pino
node logging_pino.js
```
