# Docker Logging with Fluentd — Companion Files

Runnable companion for the StackPractices recipe [Centralize Container Logs with Fluentd and Docker](https://stackpractices.com/recipes/docker-logging-fluentd/).

## Files

| File | Purpose |
|------|---------|
| `fluentd.conf` | Forward input + record_transformer/parser filters + `@type copy` fan-out to Elasticsearch and stdout |
| `fluentd-sidecar.conf` | `tail` source for apps that write to log files |
| `fluentd-s3.conf` | S3 output variant for cold log archive |
| `docker-compose.yml` | Full stack: Fluentd + Elasticsearch + Kibana + demo app on the fluentd driver |
| `docker-compose.sidecar.yml` | Sidecar variant: shared volume + file tailing |
| `Dockerfile` | Minimal image for the Node demo app |
| `server.js` | Node app emitting structured JSON logs to stdout |
| `app.py` | Python `JsonFormatter` variant |
| `verify-pipeline.sh` | End-to-end checks: Fluentd up, fluent-cat test event, ES index, sample docs |

## Quick start

```bash
docker compose up -d
docker logs -f api          # app emits JSON logs
curl localhost:9200/_cat/indices?v
./verify-pipeline.sh
```

Then open Kibana at `http://localhost:5601`, create a data view on `docker-logs-*`, and query `service:api AND level:error` in Discover.

The sidecar variant runs with `docker compose -f docker-compose.sidecar.yml up -d` — it tails `/var/log/app/app.log` through the shared `api-logs` volume instead of using the logging driver.
