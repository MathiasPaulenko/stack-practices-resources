# Distroless Docker Images with Multi-Stage Builds — Companion Files

Runnable multi-stage Dockerfiles for the recipe on
[stackpractices.com](https://stackpractices.com/recipes/docker-multi-stage-build-distroless/).

## Files

- `Dockerfile.go` — Go → `gcr.io/distroless/static-debian12` (~15MB, no shell)
- `Dockerfile.go-healthcheck` — same + `HEALTHCHECK` via the binary's own `--healthcheck` flag
- `Dockerfile.node` — Node.js → `gcr.io/distroless/nodejs22-debian12`
- `Dockerfile.python` — Python → `python:3.12-slim` multi-stage (interpreter needs its stdlib)
- `Dockerfile.java` — Gradle → `eclipse-temurin:21-jre-alpine` (swap in `distroless/java21-debian12` to go shell-free)
- `Dockerfile.alpine` — Alpine alternative when you need `sh`/`apk`
- `server.go`, `index.js`, `app.py` — demo apps
- `verify-size.sh` — builds the Go images, prints sizes, and shows `sh` fails in distroless
- `.dockerignore` — keep the build context out of layer-cache poison

## Quick start

```bash
docker build -f Dockerfile.go -t demo:distroless .
docker run -p 8080:8080 demo:distroless
curl localhost:8080
```

Debugging inside a distroless container: use the `:debug` variant
(`gcr.io/distroless/static-debian12:debug` ships busybox) or `docker cp`
tools into the running container.
