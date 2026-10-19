# Gestión de Secretos en Docker — Companion

Ejemplos ejecutables de [Gestión de Secretos Docker Sin Hardcodear Credenciales](https://stackpractices.com/es/recipes/docker-secrets-management/).

## Contenido

| Archivo | Qué muestra |
|---------|-------------|
| `docker-compose.yml` | Secrets por archivo montados en `/run/secrets/` con la convención `_FILE` |
| `Dockerfile` | `--mount=type=secret` de BuildKit para credenciales de build (nunca en capas) |
| `app.py` | Helper `get_secret()` con fallback `_FILE`, además de Vault (`hvac`), AWS (`boto3`) y caché en memoria |
| `get-secret.js` | El mismo patrón `_FILE` en Node.js |
| `rotate-secrets.sh` | Rotación de secretos sin downtime en Docker Swarm |
| `.env.example` | Plantilla de desarrollo — copiar a `.env`, que va en `.gitignore` |

## Probarlo

```bash
mkdir -p secrets
echo "local-dev-password" > secrets/db_password.txt
echo "local-dev-key" > secrets/api_key.txt
docker compose up --build
```

Asegúrate de que `.gitignore` incluya `.env`, `.env.*` y `secrets/`.
