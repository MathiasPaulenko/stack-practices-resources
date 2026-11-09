# Docker for Developers — Companion Files

The runnable files from the guide: a production multi-stage Dockerfile, a development Compose stack, and a `.dockerignore`.

Source article: [Docker for Developers — A Complete Guide](https://stackpractices.com/guides/docker-for-developers-guide/)

## Files

| File | Role |
|------|------|
| `Dockerfile` | Multi-stage build: builder compiles, runner ships only dist + prod deps, non-root user, HEALTHCHECK. |
| `docker-compose.yml` | Dev stack: api + postgres + redis, healthcheck-gated startup, bind mount + anonymous node_modules volume. |
| `.dockerignore` | Keeps `node_modules`, `.git`, `.env`, and build output out of the build context. |

## Usage

```bash
docker build -t myapp:1.0 .          # production image
docker compose up -d                  # dev stack
docker compose logs -f api            # follow app logs
docker compose down -v                # tear down, volumes included
```
