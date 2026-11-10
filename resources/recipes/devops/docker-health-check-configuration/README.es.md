# Configuración de Docker Health Check — Archivos complementarios

Versiones ejecutables de cada patrón de health check de la receta: Dockerfiles, scripts de probe, un stack de Compose con orden de arranque, un override de producción, un check de worker basado en heartbeat y un endpoint de actuator de Spring Boot.

Artículo fuente: [Configuración de Docker Health Check para Confiabilidad](https://stackpractices.com/es/recipes/docker-health-check-configuration/)

## Archivos

| Archivo | Rol |
|---------|-----|
| `Dockerfile` | Imagen Node 20 Alpine con `HEALTHCHECK` de `curl -f /health`. |
| `Dockerfile.python` | Imagen Python 3.12 slim que sondea vía `healthcheck.sh`. |
| `Dockerfile.worker` | Worker sin listener HTTP — sondea la edad del archivo heartbeat. |
| `server.js` | Servidor HTTP Node mínimo que expone `GET /health`. |
| `app.py` + `requirements.txt` | App FastAPI con `GET /health` para la imagen Python. |
| `worker.js` | Worker de cola que toca `/tmp/worker.heartbeat` cada 30s. |
| `healthcheck.sh` | Probe HTTP simple — sale con 0 si 200, con 1 si no. |
| `healthcheck-advanced.sh` | Check de varios pasos: HTTP + disco + proceso + memoria. |
| `healthcheck-logged.sh` | Probe con log de auditoría (para depurar — escribe a disco en cada ejecución). |
| `docker-compose.yml` | api + worker + redis con healthchecks y `depends_on: service_healthy`. |
| `docker-compose.prod.yml` | Ajuste de producción más estricto + check `pg_isready` de postgres. |
| `HealthController.java` + `application.yml` | Endpoint `/health` de Spring Boot + `HealthIndicator` de actuator. |

## Uso

```bash
# API Node con healthcheck de curl
docker build -t hc-api -f Dockerfile .
docker run -d -p 3000:3000 --name api hc-api
docker inspect --format='{{json .State.Health}}' api | jq

# Stack de Compose — el worker espera a que api y redis estén healthy
docker compose up -d
docker compose ps   # muestra (healthy)/(unhealthy) por servicio

# Ajuste de producción
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Notas

- `docker run` normal **no** reinicia contenedores unhealthy — el estado es informativo. Docker Swarm reemplaza las tareas unhealthy, y `willfarrell/autoheal` puede hacerlo en Docker normal.
- Kubernetes ignora `HEALTHCHECK`; define probes de liveness/readiness en el pod spec en su lugar.
