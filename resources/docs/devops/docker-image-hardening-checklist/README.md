# Docker Image Hardening Checklist — Companion Files

Runnable files for the [Docker Image Hardening Checklist](https://stackpractices.com/docs/docker-image-hardening-checklist/) on StackPractices.

## What's here

| File | Purpose |
| --- | --- |
| `Dockerfile` | Hardened multi-stage Node build: non-root UID 1001, BuildKit secret mount, clean layers |
| `.dockerignore` | Context exclusions — secrets, `.git`, node_modules, docs |
| `docker-compose.hardened.yml` | Full runtime hardening: read-only rootfs, `cap_drop: ALL`, tmpfs, network isolation, limits, secrets |
| `seccomp-profile.json` | Allowlist seccomp profile for a Node app |
| `trivy-scan.yml` | GitHub Actions pipeline: build → Trivy gate (HIGH/CRITICAL) → SBOM → Cosign sign |
| `run-hardened.sh` | One-shot `docker run` with every runtime control |
| `verify-hardening.sh` | Verification commands — each check should pass/fail closed |
| `src/server.js`, `package.json` | Minimal app so the image actually builds and runs |
| `secrets/db-password.txt` | Placeholder runtime secret (replace, never commit real values) |

## Quick start

```bash
# 1. Build the hardened image
docker build -t myapp:hardened -f Dockerfile .

# 2. Create the backend network and run hardened
docker network create backend --internal
./run-hardened.sh

# 3. Verify every control
./verify-hardening.sh myapp

# Or use the compose stack
docker compose -f docker-compose.hardened.yml up --build
```

## Scan and sign

```bash
trivy image myapp:hardened --severity HIGH,CRITICAL --exit-code 1
trivy image --format cyclonedx --output sbom.json myapp:hardened
cosign sign --yes myapp:hardened
```
