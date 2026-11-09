# Docker Compose Override por Entorno — Archivos complementarios

Un `docker-compose.yml` base más archivos override por entorno. Compose los fusiona en el orden de los `-f`: los posteriores sobrescriben o extienden a los anteriores.

Artículo fuente: [Sobrescribe la Configuración de Docker Compose por Entorno](https://stackpractices.com/es/recipes/docker-compose-override-environments/)

## Archivos

| Archivo | Rol |
|---------|-----|
| `docker-compose.yml` | Configuración base: app + postgres + redis, con valores por defecto de producción. |
| `docker-compose.override.yml` | Lo carga `docker compose up` automáticamente: hot reload, puerto de debugger, Mailpit + Adminer para dev. |
| `docker-compose.prod.yml` | Réplicas, límites de recursos, restart policy, logging JSON y Docker secrets. Se carga explícitamente. |
| `docker-compose.test.yml` | Comando `npm test`, base de datos efímera (`volumes: !reset []`), redis eliminado (`!reset null`). |
| `docker-compose.staging.yml` | Configuración de prod a menor escala: 1 réplica, límites ajustados, volumen propio. |
| `docker-compose.profiles.yml` | Servicios opcionales `debug-tools` y `load-test` detrás de flags `--profile`. |
| `.env.dev` / `.env.staging` / `.env.prod` | Archivos de variables por entorno que se cargan con `--env-file`. |
| `Makefile` | Atajos `make dev|staging|prod|test|down|logs|config` para las cadenas de `-f`. |
| `deploy.yml` | Workflow de GitHub Actions: rama → archivo override (`main`→prod, `staging`→staging). |

## Uso

```bash
# Desarrollo (fusiona base + override automáticamente)
docker compose up

# Producción
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Staging
docker compose --env-file .env.staging -f docker-compose.yml -f docker-compose.staging.yml up -d

# Tests
docker compose -f docker-compose.yml -f docker-compose.test.yml up --abort-on-container-exit

# Elegir otro archivo env
docker compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up -d

# Inspeccionar el resultado fusionado antes de levantar nada
docker compose -f docker-compose.yml -f docker-compose.prod.yml config
```

## Notas

- `!reset []` y `!reset null` vienen de la Compose Specification: eliminan valores heredados en lugar de fusionarlos — así quita el test el volumen y redis.
- Las rutas relativas siempre se resuelven respecto al directorio del archivo base.
- `.env.prod` trae valores de ejemplo: cámbialos y mantén los secrets reales fuera de git (o usa Docker secrets como en `docker-compose.prod.yml`).
