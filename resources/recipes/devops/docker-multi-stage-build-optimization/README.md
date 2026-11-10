# Docker Multi-Stage Build Optimization — Companion Files

Runnable Dockerfiles for the recipe on
[stackpractices.com](https://stackpractices.com/recipes/docker-multi-stage-build-optimization/).

## Files

- `Dockerfile.node` — Node.js two-stage build, production deps only in the final stage
- `Dockerfile.python` — `pip --target=/opt/deps` onto `distroless/python3` (no broken venv symlinks)
- `Dockerfile.go` — static Go binary on `scratch` (~15MB total)
- `Dockerfile.java` — Gradle → `eclipse-temurin:21-jre-alpine` with a real created user
- `Dockerfile.rust` — Rust → `debian:bookworm-slim`
- `Dockerfile.test-stages` — deps/test/build/production pipeline; `docker build --target test .` runs CI only
- `Dockerfile.multiarch` — `$BUILDPLATFORM`/`$TARGETPLATFORM` for `buildx` amd64+arm64
- `Dockerfile.cache-mounts` — BuildKit `--mount=type=cache` for npm/pip/Go modules
- `server.go`, `index.js`, `app.py` — demo apps for each runtime
- `verify-size.sh` — builds the Go image and prints sizes + layer breakdown
- `.dockerignore` — keep `node_modules`/`.git` out of the build context

## Quick start

```bash
docker build -f Dockerfile.go -t msdemo:scratch .
docker run -p 8080:8080 msdemo:scratch
curl localhost:8080
```

Run only the test stage (CI, nothing published):

```bash
docker build -f Dockerfile.test-stages --target test .
```
