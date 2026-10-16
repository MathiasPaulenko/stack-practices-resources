# Patrón Health Check — Demo ejecutable

Código acompañante del recurso de StackPractices
[Patrón Health Check: Sondeos de Liveness y Readiness](https://stackpractices.com/es/patterns/health-check-pattern/).

Un servicio FastAPI pequeño que expone los tres endpoints de probe que Kubernetes
espera, con dependencias reales (PostgreSQL, Redis) para ver cómo readiness cambia
entre 200 y 503 cuando una dependencia se cae.

## Archivos

| Archivo | Qué muestra |
|---|---|
| `app.py` | `/health/live`, `/health/ready`, `/health/startup` con chequeos de dependencias y apagado elegante vía `lifespan` |
| `worker_probe.py` | Probe por comando (`exec`) para workers sin servidor HTTP |
| `k8s-deployment.yaml` | Deployment con los tres tipos de probe y timings razonables |
| `docker-compose.yml` | Laboratorio local: app + PostgreSQL + Redis con `HEALTHCHECK` y condiciones en `depends_on` |
| `Dockerfile`, `requirements.txt` | Build del contenedor de la demo |

## Probarlo

```bash
docker compose up --build

curl -i localhost:8080/health/live      # 200 — el proceso está vivo
curl -i localhost:8080/health/ready     # 200 cuando postgres + redis están arriba
docker compose stop postgres            # readiness pasa a 503, liveness sigue en 200
docker compose start postgres           # readiness se recupera
```

En Kubernetes: construye la imagen como `health-check-demo:1.0.0` y aplica
`k8s-deployment.yaml`. El `startupProbe` le da a la app hasta 150 segundos para
arrancar antes de que liveness tome el control.
