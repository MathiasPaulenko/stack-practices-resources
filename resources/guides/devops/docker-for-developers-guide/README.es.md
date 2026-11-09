# Docker para Desarrolladores — Archivos complementarios

Los archivos ejecutables de la guía: un Dockerfile multi-etapa para producción, un stack Compose de desarrollo y un `.dockerignore`.

Artículo fuente: [Docker para Desarrolladores — Guía Completa](https://stackpractices.com/es/guides/docker-for-developers-guide/)

## Archivos

| Archivo | Rol |
|---------|-----|
| `Dockerfile` | Build multi-etapa: builder compila, runner solo lleva dist + deps de prod, usuario no-root, HEALTHCHECK. |
| `docker-compose.yml` | Stack de dev: api + postgres + redis, arranque condicionado por healthcheck, bind mount + volumen anónimo de node_modules. |
| `.dockerignore` | Mantiene `node_modules`, `.git`, `.env` y la salida de build fuera del contexto. |

## Uso

```bash
docker build -t myapp:1.0 .          # imagen de producción
docker compose up -d                  # stack de desarrollo
docker compose logs -f api            # sigue los logs de la app
docker compose down -v                # tumba todo, volúmenes incluidos
```
