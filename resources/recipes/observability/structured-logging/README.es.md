# Logging Estructurado — Ejemplos de Código

Código complementario de [Logging estructurado: logs JSON con correlation IDs](https://stackpractices.com/es/recipes/structured-logging/) en StackPractices.

## Archivos

| Archivo | Descripción |
|---|---|
| `pino_logger.js` | Logger JSON con Pino con child loggers y correlation IDs (Node.js) |
| `structlog_setup.py` | Pipeline de structlog con timestamps ISO y renderizado JSON (Python) |
| `correlation_middleware.go` | Middleware de propagación `X-Request-ID` (Go) |
| `example_output.json` | Líneas de log estructurado de ejemplo emitidas por un handler |
| `fluent-bit.conf` | Configuración de pipeline Fluent Bit tail → Loki |
| `pino_redact.js` | Redacción de campos con `redact` paths de pino |
