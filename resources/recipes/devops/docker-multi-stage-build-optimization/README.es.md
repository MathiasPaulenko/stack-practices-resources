# Optimización de Multi-Stage Builds en Docker — Archivos complementarios

Dockerfiles ejecutables para la receta en
[stackpractices.com](https://stackpractices.com/es/recipes/docker-multi-stage-build-optimization/).

## Archivos

- `Dockerfile.node` — build Node.js de dos etapas, solo deps de producción en la final
- `Dockerfile.python` — `pip --target=/opt/deps` sobre `distroless/python3` (sin symlinks rotos de venv)
- `Dockerfile.go` — binario Go estático sobre `scratch` (~15MB total)
- `Dockerfile.java` — Gradle → `eclipse-temurin:21-jre-alpine` con usuario creado de verdad
- `Dockerfile.rust` — Rust → `debian:bookworm-slim`
- `Dockerfile.test-stages` — pipeline deps/test/build/production; `docker build --target test .` corre solo CI
- `Dockerfile.multiarch` — `$BUILDPLATFORM`/`$TARGETPLATFORM` para `buildx` amd64+arm64
- `Dockerfile.cache-mounts` — `--mount=type=cache` de BuildKit para npm/pip/módulos Go
- `server.go`, `index.js`, `app.py` — apps de demo para cada runtime
- `verify-size.sh` — construye la imagen Go e imprime tamaños + desglose por capas
- `.dockerignore` — deja `node_modules`/`.git` fuera del contexto de build

## Inicio rápido

```bash
docker build -f Dockerfile.go -t msdemo:scratch .
docker run -p 8080:8080 msdemo:scratch
curl localhost:8080
```

Corre solo la etapa de test (CI, sin publicar nada):

```bash
docker build -f Dockerfile.test-stages --target test .
```
