# Log Aggregation — Fluent Bit → Loki Pipeline

Companion runnable example for the guide
[Complete Guide to Log Aggregation](https://stackpractices.com/guides/log-aggregation-guide/).

A minimal end-to-end log pipeline: a Node.js app writes structured JSON logs,
a Fluent Bit agent tails and enriches them, Loki stores them, and Grafana
exposes the query UI.

## Stack

| Component | Role |
|-----------|------|
| `app/` | Node.js demo emitting structured JSON logs (pino) |
| `fluent-bit.conf` | Agent: tail → enrich (service/environment) → ship to Loki |
| Loki | Log store (label-indexed chunks) |
| Grafana | Query UI with LogQL |

## Run

```bash
docker compose up -d --build
docker compose logs -f fluent-bit   # watch the shipper
```

Open Grafana at http://localhost:3000, add Loki as a data source
(`http://loki:3100`), then query in Explore:

```logql
{service="demo-service"} |= "request_handled"
sum(rate({service="demo-service"} |= "error" [1m]))
{service="demo-service"} |= "request_handled" | json | duration_ms > 400
```

## What it demonstrates

- Structured JSON logging from the app (guide step 1)
- Agent-per-node shipping with a `tail` input and record enrichment (step 2)
- Label-based indexing in Loki and LogQL queries (step 4)
- Disk-buffered tail input (`DB`) that survives restarts
