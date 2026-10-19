# Docker Secrets Management — Companion

Runnable examples for [Docker Secrets Management Without Hardcoding Credentials](https://stackpractices.com/recipes/docker-secrets-management/).

## Contents

| File | What it shows |
|------|---------------|
| `docker-compose.yml` | File-based secrets mounted at `/run/secrets/` with the `_FILE` convention |
| `Dockerfile` | BuildKit `--mount=type=secret` for build-time credentials (never in layers) |
| `app.py` | `get_secret()` helper with `_FILE` fallback, plus Vault (`hvac`), AWS (`boto3`), and in-memory caching |
| `get-secret.js` | Same `_FILE` pattern in Node.js |
| `rotate-secrets.sh` | Zero-downtime secret rotation on Docker Swarm |
| `.env.example` | Development template — copy to `.env`, which stays in `.gitignore` |

## Try it

```bash
mkdir -p secrets
echo "local-dev-password" > secrets/db_password.txt
echo "local-dev-key" > secrets/api_key.txt
docker compose up --build
```

Make sure `.gitignore` contains `.env`, `.env.*`, and `secrets/`.
