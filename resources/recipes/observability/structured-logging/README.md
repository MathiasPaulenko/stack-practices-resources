# Structured Logging — Code Examples

Companion code for [Structured Logging: JSON Logs with Correlation IDs](https://stackpractices.com/recipes/structured-logging/) on StackPractices.

## Files

| File | Description |
|---|---|
| `pino_logger.js` | Pino JSON logger with child loggers and correlation IDs (Node.js) |
| `structlog_setup.py` | structlog pipeline with ISO timestamps and JSON rendering (Python) |
| `correlation_middleware.go` | `X-Request-ID` propagation middleware (Go) |
| `example_output.json` | Sample structured log lines emitted by a handler |
| `fluent-bit.conf` | Fluent Bit tail → Loki pipeline config |
| `pino_redact.js` | Field redaction with pino `redact` paths |
