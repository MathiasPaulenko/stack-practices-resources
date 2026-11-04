# Complete Guide to Docker in Production — Companion Assets

Production-ready Docker files from the
[Complete Guide to Docker in Production](https://stackpractices.com/guides/complete-guide-docker-production/).

## Contents

| File | What it shows |
| --- | --- |
| `Dockerfile.python-multi-stage` | Builder → distroless runtime (Python/uvicorn) |
| `Dockerfile.node-multi-stage` | Three-stage deps → build → slim runtime with HEALTHCHECK |
| `Dockerfile.distroless-go` | Static Go binary on `static-debian12:nonroot` |
| `docker-compose.prod.yml` | Limits, healthcheck, log rotation, read-only, internal network |
| `.dockerignore` | Build-context hygiene (`.git`, tests, node_modules) |
| `scan-image.sh` | Build + Trivy HIGH/CRITICAL gate for CI |

## Usage

```bash
# Build the Python image
cp Dockerfile.python-multi-stage Dockerfile && docker build -t myapp:latest .

# Scan gate
./scan-image.sh myapp:latest

# Production compose
docker compose -f docker-compose.prod.yml up -d
```
