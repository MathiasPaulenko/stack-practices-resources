# Log Aggregation — Runnable Examples

Runnable companion for the [Log Aggregation recipe](https://stackpractices.com/recipes/log-aggregation/) on StackPractices.

## Contents

| File | What it is |
| --- | --- |
| `docker-compose.yml` | Fluentd → Elasticsearch → Kibana stack with a persistent buffer volume |
| `fluent.conf` | Forward input, JSON parsing filter, Elasticsearch output with file buffering and exponential-backoff retries |
| `app/logger.js` | Winston structured logger emitting JSON lines with `traceId` correlation |
| `app/package.json` | Minimal Node project (`winston` only) |

## Run the stack

```bash
docker compose up -d
# Kibana → http://localhost:5601  |  Elasticsearch → http://localhost:9200
```

Send a test log through Fluentd's forward protocol:

```bash
echo '{"log":"{\"level\":\"info\",\"event\":\"test\",\"service\":\"demo\"}"}' | \
  docker exec -i $(docker ps -qf ancestor=fluent/fluentd:v1.16) fluent-cat app.demo
```

Then create the `app-*` index pattern in Kibana to explore it.

## Run the logger

```bash
cd app
npm install
npm start
```

It writes three correlated JSON lines to stdout and `app.log` — the shape a Fluent Bit tail or Promtail scrape expects.
