# Health Check Endpoint — Companion

Runnable examples for the [Health Check Endpoint recipe](https://stackpractices.com/recipes/health-check-endpoint/).

Each file implements the probe model used by Kubernetes and load balancers:

| Probe | Endpoint | Answers | Failure action |
| --- | --- | --- | --- |
| Liveness | `/health/live` | Is the process alive? | Restart container |
| Readiness | `/health/ready` | Can it serve traffic? | Remove from rotation |
| Startup | `/health/startup` | Did init finish? | Delay other probes |

## Files

- `health_check.py` — FastAPI version with lifespan-based startup flag. Needs `DATABASE_URL` and optionally `REDIS_URL`.
- `health_check.js` — Express version with `pg` Pool. Needs `DATABASE_URL`.
- `main.go` — net/http version with `database/sql` + go-redis and `atomic.Bool` startup flag.
- `DatabaseHealthIndicator.java` — Spring Boot Actuator `HealthIndicator` for the database; pair with `management.endpoint.health.probes.enabled=true`.
- `k8s-deployment.yaml` — Deployment wiring liveness/readiness/startup probes to the three endpoints.
- `docker-compose.yml` — Compose `healthcheck` + `depends_on: condition: service_healthy`.

## Quick start

```bash
# Python
pip install fastapi uvicorn psycopg2-binary redis
DATABASE_URL=postgres://user:pass@localhost/db uvicorn health_check:app --port 8080

# Node.js
npm install express pg
DATABASE_URL=postgres://user:pass@localhost/db node health_check.js

# Go
go mod init example.com/healthcheck
go get github.com/lib/pq github.com/redis/go-redis/v9
go run main.go
```

Then probe them:

```bash
curl -i localhost:8080/health/live     # 200 {"status":"alive"}
curl -i localhost:8080/health/startup  # 200 once init succeeds, 503 before
curl -i localhost:8080/health/ready    # 200 ready / 503 not ready + per-dep checks
```
