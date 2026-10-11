# Structured Logging — Recursos companion

Código companion del [patrón Structured Logging](https://stackpractices.com/es/patterns/structured-logging-pattern/) en StackPractices.

## Archivos

| Archivo | Lenguaje | Descripción |
| --- | --- | --- |
| `structlog_example.py` | Python 3.10+ | Configuración de structlog: renderer JSON, contexto bindeado por request y processor de redacción de campos sensibles |
| `json_formatter.py` | Python 3.10+ | `logging.Formatter` sin dependencias que emite una línea JSON por registro |
| `async_logging.py` | Python 3.10+ | Par `QueueHandler`/`QueueListener` para logging no bloqueante en caminos calientes |
| `logging_pino.js` | Node.js 20+ | Configuración de pino: timestamps ISO, metadata base, child loggers y sampling por endpoint |
| `test_structured_logging.py` | Python + pytest | Verifica la forma de la salida JSON, la redacción, el contexto bindeado y la entrega por queue |

## Inicio rápido

### Python (pytest)

```bash
pip install structlog pytest
pytest test_structured_logging.py
```

### Ejemplos en Python

```bash
python structlog_example.py   # contexto bindeado + redacción
python json_formatter.py      # formatter JSON de stdlib
python async_logging.py       # logging no bloqueante con queue
```

### Node.js (pino)

```bash
npm install pino
node logging_pino.js
```
