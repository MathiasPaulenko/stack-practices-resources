# Health Check Endpoint — Recursos complementarios

Ejemplos ejecutables de la [receta Health Check Endpoint](https://stackpractices.com/es/recipes/health-check-endpoint/).

Cada archivo implementa el modelo de probes usado por Kubernetes y load balancers:

| Probe | Endpoint | Responde | Acción al fallar |
| --- | --- | --- | --- |
| Liveness | `/health/live` | ¿El proceso está vivo? | Reiniciar contenedor |
| Readiness | `/health/ready` | ¿Puede servir tráfico? | Quitar de rotación |
| Startup | `/health/startup` | ¿Terminó la inicialización? | Retrasar otros probes |

## Archivos

- `health_check.py` — versión FastAPI con flag de startup vía lifespan. Necesita `DATABASE_URL` y opcionalmente `REDIS_URL`.
- `health_check.js` — versión Express con `pg` Pool. Necesita `DATABASE_URL`.
- `main.go` — versión net/http con `database/sql` + go-redis y flag de startup con `atomic.Bool`.
- `DatabaseHealthIndicator.java` — `HealthIndicator` de Spring Boot Actuator para la base de datos; combinar con `management.endpoint.health.probes.enabled=true`.
- `k8s-deployment.yaml` — Deployment que conecta los probes de liveness/readiness/startup con los tres endpoints.
- `docker-compose.yml` — `healthcheck` de Compose + `depends_on: condition: service_healthy`.

## Inicio rápido

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

Luego sondea los endpoints:

```bash
curl -i localhost:8080/health/live     # 200 {"status":"alive"}
curl -i localhost:8080/health/startup  # 200 cuando init termina, 503 antes
curl -i localhost:8080/health/ready    # 200 ready / 503 not ready + checks por dep
```
