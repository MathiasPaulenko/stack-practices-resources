# Guía Completa de Docker en Producción — Assets del ejemplo

Archivos Docker listos para producción de la
[Guía Completa de Docker en Producción](https://stackpractices.com/es/guides/complete-guide-docker-production/).

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `Dockerfile.python-multi-stage` | Builder → runtime distroless (Python/uvicorn) |
| `Dockerfile.node-multi-stage` | Tres stages deps → build → runtime slim con HEALTHCHECK |
| `Dockerfile.distroless-go` | Binario Go estático sobre `static-debian12:nonroot` |
| `docker-compose.prod.yml` | Límites, healthcheck, rotación de logs, read-only, red interna |
| `.dockerignore` | Higiene del contexto (`.git`, tests, node_modules) |
| `scan-image.sh` | Build + gate de Trivy HIGH/CRITICAL para CI |

## Uso

```bash
# Construir la imagen Python
cp Dockerfile.python-multi-stage Dockerfile && docker build -t myapp:latest .

# Gate de escaneo
./scan-image.sh myapp:latest

# Compose de producción
docker compose -f docker-compose.prod.yml up -d
```
