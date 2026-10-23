# Docker Compose Local Dev — Archivos del Companion

Archivos ejecutables de la guía
[Docker Compose: Desarrollo Local Multi-Servicio](https://stackpractices.com/es/guides/complete-guide-docker-compose-local-dev/)
([English version](https://stackpractices.com/guides/complete-guide-docker-compose-local-dev/)).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `docker-compose.yml` | Stack completo: frontend, backend, worker, postgres, redis, nginx + `mailhog` bajo el profile `debug` |
| `docker-compose.override.yml` | Overrides de dev auto-cargados (variables de depuración) |
| `docker-compose.prod.yml` | Configuración tipo producción — uso con `-f` explícito |
| `docker-compose.test.yml` | Entorno de test — listo para CI con `--exit-code-from` |
| `Dockerfile.dev` | Imagen mínima de desarrollo (código por bind mount, sin hardening) |
| `start-dev.sh` | Primer arranque: build, espera a la DB sana, migra, siembra |
| `seed-dev.sh` | Reinicia el schema y re-siembra datos de demo |
| `Makefile` | `make up / down / logs / test / shell / db-shell` |

## Uso

```bash
chmod +x start-dev.sh seed-dev.sh
./start-dev.sh                 # primer arranque
make up                        # arranque diario
docker compose --profile debug up   # con mailhog
```

Sustituye los contextos `frontend`/`backend` por tus directorios reales. Mantén los valores tipo `JWT_SECRET` en un `.env` fuera de git.
