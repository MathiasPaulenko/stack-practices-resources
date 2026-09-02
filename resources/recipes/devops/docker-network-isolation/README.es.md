# Aislamiento de Red Docker — Recursos Companion

Configuración de Docker Compose de tres capas que demuestra aislamiento de red:

- **web** (nginx) en la red `frontend`, puerto 8080
- **api** (Node.js/Express) en las redes `frontend` y `backend`
- **db** (PostgreSQL 16) en la red `backend` (interna, sin internet)

## Topología de red

```
Internet -> web (frontend) -> api (frontend + backend) -> db (backend, interna)
```

El contenedor web no puede alcanzar la base de datos directamente — no comparten
ninguna red. La API une ambas redes, actuando como el único camino entre ellas.

## Inicio rápido

```bash
docker compose up -d

# Probar desde afuera
curl http://localhost:8080/

# Probar conectividad desde dentro de un contenedor
docker compose exec api sh -c "wget -qO- http://db:5432 || echo 'db alcanzable en puerto 5432'"

# Verificar que web no puede alcanzar db
docker compose exec web sh -c "wget -qO- http://db:5432 2>&1 || echo 'web no alcanza db (esperado)'"
```

## Verificar aislamiento

```bash
# Listar redes
docker network ls | grep docker-network-isolation

# Inspeccionar la red backend (debería ser interna)
docker network inspect docker-network-isolation_backend

# Intentar alcanzar internet desde el contenedor db (debería fallar)
docker compose exec db sh -c "wget -qO- https://example.com 2>&1 || echo 'sin internet (esperado)'"
```

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `docker-compose.yml` | Definición de servicios de tres capas con redes aisladas |
| `Dockerfile` | API stub en Node.js/Express que se conecta a PostgreSQL |
| `nginx.conf` | Configuración de reverse proxy para el contenedor web |
| `init-db.sh` | Script de inicialización de PostgreSQL |

## Fuente

- [Receta en inglés](https://stackpractices.com/recipes/docker-network-isolation/)
- [Receta en español](https://stackpractices.com/es/recipes/docker-network-isolation/)
