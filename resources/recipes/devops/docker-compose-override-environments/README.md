# Docker Compose Override Environments — Companion Files

One base `docker-compose.yml` plus per-environment override files. Compose merges them in `-f` order; later files override or extend earlier ones.

Source article: [Override Docker Compose Configs per Environment](https://stackpractices.com/recipes/docker-compose-override-environments/)

## Files

| File | Role |
|------|------|
| `docker-compose.yml` | Base config: app + postgres + redis, production-shaped defaults. |
| `docker-compose.override.yml` | Auto-loaded by `docker compose up` — hot reload, debugger port, Mailpit + Adminer for local dev. |
| `docker-compose.prod.yml` | Replicas, resource limits, restart policy, JSON logging, and Docker secrets. Loaded explicitly. |
| `docker-compose.test.yml` | `npm test` command, ephemeral DB (`volumes: !reset []`), redis removed (`!reset null`). |
| `docker-compose.staging.yml` | Prod-shaped config at smaller scale: replicas 1, tighter limits, own data volume. |
| `docker-compose.profiles.yml` | Optional `debug-tools` and `load-test` services behind `--profile` flags. |
| `.env.dev` / `.env.staging` / `.env.prod` | Per-environment variable files loaded with `--env-file`. |
| `Makefile` | `make dev|staging|prod|test|down|logs|config` shortcuts for the `-f` chains. |
| `deploy.yml` | GitHub Actions workflow: branch → override file mapping (`main`→prod, `staging`→staging). |

## Usage

```bash
# Development (auto-merges base + override)
docker compose up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Staging
docker compose --env-file .env.staging -f docker-compose.yml -f docker-compose.staging.yml up -d

# Tests
docker compose -f docker-compose.yml -f docker-compose.test.yml up --abort-on-container-exit

# Pick a different env file
docker compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up -d

# Inspect the merged result before running anything
docker compose -f docker-compose.yml -f docker-compose.prod.yml config
```

## Notes

- `!reset []` and `!reset null` come from the Compose Specification — they delete inherited values instead of merging, which is how the test file drops the volume and redis.
- Relative paths always resolve against the base file's directory.
- `.env.prod` ships placeholder values — replace them and keep real secrets out of git (or use Docker secrets as in `docker-compose.prod.yml`).
