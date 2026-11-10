# Docker Health Check Configuration — Companion Files

Runnable versions of every health check pattern from the recipe: Dockerfiles, probe scripts, a Compose stack with startup ordering, a production override, a heartbeat-based worker check, and a Spring Boot actuator endpoint.

Source article: [Docker Health Check Configuration for Container Reliability](https://stackpractices.com/recipes/docker-health-check-configuration/)

## Files

| File | Role |
|------|------|
| `Dockerfile` | Node 20 Alpine image with a `curl -f /health` `HEALTHCHECK`. |
| `Dockerfile.python` | Python 3.12 slim image probing via `healthcheck.sh`. |
| `Dockerfile.worker` | Worker without HTTP listener — probes heartbeat-file age. |
| `server.js` | Minimal Node HTTP server exposing `GET /health`. |
| `app.py` + `requirements.txt` | FastAPI app exposing `GET /health` for the Python image. |
| `worker.js` | Queue worker that touches `/tmp/worker.heartbeat` every 30s. |
| `healthcheck.sh` | Simple HTTP probe — exits 0 on 200, 1 otherwise. |
| `healthcheck-advanced.sh` | Multi-step check: HTTP + disk + process + memory. |
| `healthcheck-logged.sh` | Probe with audit log (debugging use — it writes to disk each run). |
| `docker-compose.yml` | api + worker + redis with healthchecks and `depends_on: service_healthy`. |
| `docker-compose.prod.yml` | Tighter production tuning + postgres `pg_isready` check. |
| `HealthController.java` + `application.yml` | Spring Boot `/health` endpoint + actuator `HealthIndicator`. |

## Usage

```bash
# Node API with curl healthcheck
docker build -t hc-api -f Dockerfile .
docker run -d -p 3000:3000 --name api hc-api
docker inspect --format='{{json .State.Health}}' api | jq

# Compose stack — worker waits for api and redis to be healthy
docker compose up -d
docker compose ps   # shows (healthy)/(unhealthy) per service

# Production tuning
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Notes

- Plain `docker run` does **not** restart unhealthy containers — the status is informational. Docker Swarm replaces unhealthy tasks, and `willfarrell/autoheal` can do it on plain Docker.
- Kubernetes ignores `HEALTHCHECK`; define liveness/readiness probes in the pod spec instead.
