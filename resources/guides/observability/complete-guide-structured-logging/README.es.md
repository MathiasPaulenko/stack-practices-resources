# Logging Estructurado — Ejemplos Ejecutables

Companion de [Logging Estructurado: JSON, IDs de Correlación y Agregación](https://stackpractices.com/es/guides/complete-guide-structured-logging/).

## Contenido

| Archivo | Qué muestra |
|---|---|
| `logging_config.py` | Setup de structlog con inyección de service/env vía `bind_contextvars`, parámetros de callsite, renderer JSON y enrutado del handler stdlib |
| `middleware.py` | `CorrelationIdMiddleware` para Starlette — genera/propaga `X-Request-ID`, vincula `request_id`/`user_id` a los contextvars de structlog |
| `order_service.py` | Logging de lógica de negocio con nombres de evento snake_case y campos estructurados |
| `logger.ts` | Config de pino — timestamps ISO, formato de nivel, `mixin` + `AsyncLocalStorage` para correlación automática, `redact.paths` |
| `middleware.ts` | Middleware de correlación para Express — scope con `AsyncLocalStorage.run`, timing de requests |
| `service.ts` | Loggers hijos de pino con campo `service` vinculado |
| `CorrelationIdFilter.java` | Filtro servlet que pone `request_id`/`user_id` en MDC con el `MDC.clear()` obligatorio en `finally` |
| `logback.xml` | Config de `LogstashEncoder` — salida JSON con custom fields de service/env |
| `docker-compose-elk.yml` + `logstash.conf` | Stack Elasticsearch + Logstash + Kibana que parsea JSON desde Filebeat |
| `docker-compose-loki.yml` + `promtail-config.yml` | Loki + Grafana + Promtail con pipeline JSON — labels limitadas a baja cardinalidad |

## Correr el ejemplo Python

```bash
pip install -r requirements.txt
python logging_config.py
```

Emite dos líneas JSON mostrando los campos `service`/`env` inyectados y el `request_id`/`user_id` vinculado.

## Levantar un stack de agregación

```bash
# ELK — Elasticsearch en :9200, Kibana en :5601, entrada beats de Logstash :5044
docker compose -f docker-compose-elk.yml up

# Loki — Grafana en :3000 (admin/admin), Loki en :3100
docker compose -f docker-compose-loki.yml up
```

Apuntá la salida de logs de tu app a `/var/log/app/*.log` (promtail) o Filebeat → Logstash `:5044` (ELK), y después consultá con KQL o LogQL como muestra la guía.
