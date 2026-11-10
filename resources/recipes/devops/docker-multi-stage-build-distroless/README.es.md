# Imágenes Docker Distroless con Multi-Stage Builds — Archivos complementarios

Dockerfiles multi-stage ejecutables para la receta en
[stackpractices.com](https://stackpractices.com/es/recipes/docker-multi-stage-build-distroless/).

## Archivos

- `Dockerfile.go` — Go → `gcr.io/distroless/static-debian12` (~15MB, sin shell)
- `Dockerfile.go-healthcheck` — igual + `HEALTHCHECK` vía el flag `--healthcheck` del binario
- `Dockerfile.node` — Node.js → `gcr.io/distroless/nodejs22-debian12`
- `Dockerfile.python` — Python → `python:3.12-slim` multi-stage (el intérprete necesita su stdlib)
- `Dockerfile.java` — Gradle → `eclipse-temurin:21-jre-alpine` (cambia a `distroless/java21-debian12` para base sin shell)
- `Dockerfile.alpine` — alternativa Alpine cuando necesitas `sh`/`apk`
- `server.go`, `index.js`, `app.py` — apps de demostración
- `verify-size.sh` — construye las imágenes Go, imprime tamaños y muestra que `sh` falla en distroless
- `.dockerignore` — mantiene el build context fuera de la caché de capas

## Inicio rápido

```bash
docker build -f Dockerfile.go -t demo:distroless .
docker run -p 8080:8080 demo:distroless
curl localhost:8080
```

Para depurar dentro de un contenedor distroless: usa la variante `:debug`
(`gcr.io/distroless/static-debian12:debug` incluye busybox) o mete
herramientas con `docker cp` en el contenedor corriendo.
