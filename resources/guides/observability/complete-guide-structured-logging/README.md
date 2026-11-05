# Structured Logging — Runnable Examples

Companion to [Structured Logging: JSON Logs, Correlation IDs, Aggregation](https://stackpractices.com/guides/complete-guide-structured-logging/).

## Contents

| File | What it shows |
|---|---|
| `logging_config.py` | structlog setup with service/env injection via `bind_contextvars`, callsite params, JSON renderer, and stdlib handler routing |
| `middleware.py` | Starlette `CorrelationIdMiddleware` — generates/propagates `X-Request-ID`, binds `request_id`/`user_id` to structlog contextvars |
| `order_service.py` | Business-logic logging with snake_case event names and structured fields |
| `logger.ts` | pino config — ISO timestamps, level formatting, `mixin` + `AsyncLocalStorage` for automatic correlation, `redact.paths` |
| `middleware.ts` | Express correlation middleware — `AsyncLocalStorage.run` scoping, request timing |
| `service.ts` | pino child loggers with bound `service` field |
| `CorrelationIdFilter.java` | Servlet filter putting `request_id`/`user_id` into MDC with the mandatory `MDC.clear()` in `finally` |
| `logback.xml` | `LogstashEncoder` config — JSON output with service/env custom fields |
| `docker-compose-elk.yml` + `logstash.conf` | Elasticsearch + Logstash + Kibana stack that parses JSON from Filebeat |
| `docker-compose-loki.yml` + `promtail-config.yml` | Loki + Grafana + Promtail with a JSON pipeline — labels kept to low cardinality |

## Run the Python example

```bash
pip install -r requirements.txt
python logging_config.py
```

Emits two JSON lines showing the injected `service`/`env` fields and the bound `request_id`/`user_id`.

## Spin up an aggregation stack

```bash
# ELK — Elasticsearch on :9200, Kibana on :5601, Logstash beats input :5044
docker compose -f docker-compose-elk.yml up

# Loki — Grafana on :3000 (admin/admin), Loki on :3100
docker compose -f docker-compose-loki.yml up
```

Point your app's log output at `/var/log/app/*.log` (promtail) or Filebeat → Logstash `:5044` (ELK), then query with KQL or LogQL as shown in the guide.
