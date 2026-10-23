# Docker Compose Local Dev — Companion Files

Runnable files for the guide
[Docker Compose: Multi-Service Local Development](https://stackpractices.com/guides/complete-guide-docker-compose-local-dev/)
([versión en español](https://stackpractices.com/es/guides/complete-guide-docker-compose-local-dev/)).

## Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Full stack: frontend, backend, worker, postgres, redis, nginx + `mailhog` under the `debug` profile |
| `docker-compose.override.yml` | Auto-loaded dev overrides (debug env vars) |
| `docker-compose.prod.yml` | Production-like config — explicit `-f` usage |
| `docker-compose.test.yml` | Test environment — CI-ready with `--exit-code-from` |
| `Dockerfile.dev` | Minimal dev image (bind-mount source, no production hardening) |
| `start-dev.sh` | First boot: build, wait for healthy DB, migrate, seed |
| `seed-dev.sh` | Reset schema + re-seed demo data |
| `Makefile` | `make up / down / logs / test / shell / db-shell` |

## Usage

```bash
chmod +x start-dev.sh seed-dev.sh
./start-dev.sh                 # first boot
make up                        # daily start
docker compose --profile debug up   # with mailhog
```

Swap the `frontend`/`backend` contexts for your real directories. Keep `JWT_SECRET`-style values in a `.env` that stays out of git.
