# Docker Network Isolation — Companion Resources

Three-tier Docker Compose setup demonstrating network isolation:

- **web** (nginx) on `frontend` network, port 8080
- **api** (Node.js/Express) on both `frontend` and `backend` networks
- **db** (PostgreSQL 16) on `backend` network (internal, no internet)

## Network topology

```
Internet -> web (frontend) -> api (frontend + backend) -> db (backend, internal)
```

The web container cannot reach the database directly — they share no network.
The API bridges both networks, acting as the only path between them.

## Quick start

```bash
docker compose up -d

# Test from outside
curl http://localhost:8080/

# Test connectivity from inside a container
docker compose exec api sh -c "wget -qO- http://db:5432 || echo 'db reachable on port 5432'"

# Verify web cannot reach db
docker compose exec web sh -c "wget -qO- http://db:5432 2>&1 || echo 'web cannot reach db (expected)'"
```

## Verify isolation

```bash
# List networks
docker network ls | grep docker-network-isolation

# Inspect the backend network (should be internal)
docker network inspect docker-network-isolation_backend

# Try reaching the internet from the db container (should fail)
docker compose exec db sh -c "wget -qO- https://example.com 2>&1 || echo 'no internet (expected)'"
```

## Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Three-tier service definition with isolated networks |
| `Dockerfile` | Node.js/Express API stub that connects to PostgreSQL |
| `nginx.conf` | Reverse proxy config for the web container |
| `init-db.sh` | PostgreSQL initialization script |

## Source

- [English recipe](https://stackpractices.com/recipes/docker-network-isolation/)
- [Spanish recipe](https://stackpractices.com/es/recipes/docker-network-isolation/)
