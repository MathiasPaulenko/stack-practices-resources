# Health Check Pattern — Runnable Demo

Companion code for the StackPractices resource
[Health Check Pattern: Expose Liveness and Readiness Probes](https://stackpractices.com/patterns/health-check-pattern/).

A small FastAPI service that exposes the three probe endpoints Kubernetes expects,
plus real dependencies (PostgreSQL, Redis) so you can watch readiness flip between
200 and 503 when a dependency goes down.

## Files

| File | What it shows |
|---|---|
| `app.py` | `/health/live`, `/health/ready`, `/health/startup` with dependency checks and graceful shutdown via `lifespan` |
| `worker_probe.py` | Command-based (`exec`) probe for workers without an HTTP server |
| `k8s-deployment.yaml` | Deployment wiring all three probe types with sane timings |
| `docker-compose.yml` | Local lab: app + PostgreSQL + Redis with `HEALTHCHECK` and `depends_on` conditions |
| `Dockerfile`, `requirements.txt` | Container build for the demo |

## Try it

```bash
docker compose up --build

curl -i localhost:8080/health/live      # 200 — process is alive
curl -i localhost:8080/health/ready     # 200 once postgres + redis are up
docker compose stop postgres            # readiness flips to 503, liveness stays 200
docker compose start postgres           # readiness recovers
```

On Kubernetes: build the image as `health-check-demo:1.0.0` and apply
`k8s-deployment.yaml`. The `startupProbe` gives the app up to 150 seconds to boot
before liveness takes over.
