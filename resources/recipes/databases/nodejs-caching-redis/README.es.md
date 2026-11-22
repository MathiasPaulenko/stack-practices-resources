# Caché con Redis en Node.js — Companion

Ejemplo ejecutable del recurso de StackPractices
[Caché en Node.js con Redis: Cache-Aside y TTL](https://stackpractices.com/es/recipes/nodejs-caching-redis/).

## Qué incluye

| Archivo | Propósito |
|---|---|
| `app.js` | App Express con cache-aside + lock (protección contra stampede), invalidación por tags y endpoint `/metrics` con el hit rate |
| `docker-compose.yml` | Redis 7 (`allkeys-lru`, límite de 128MB) más la UI Redis Commander |
| `package.json` | Dependencias `express` + `ioredis` |

## Inicio rápido

```bash
docker compose up -d
npm install
node app.js

curl http://localhost:3000/api/users/1      # database — primera petición
curl http://localhost:3000/api/users/1      # cache — segunda petición
curl http://localhost:3000/metrics          # { hits: 1, misses: 1, hitRate: "50.0%" }
curl -X POST http://localhost:3000/api/users/1/refresh   # invalida el tag
```

Redis Commander corre en http://localhost:8081 para inspeccionar claves en vivo.

## Notas

- `getOrSet` toma un `lock:${key}` con `SET NX EX` para que una clave
  caliente que expira no desate un stampede contra la "base de datos" —
  el resto de llamadas reintenta a los 100ms.
- `fetchUser` duerme 150ms simulando una query lenta; la segunda llamada
  al mismo id debería volver en milisegundos de un dígito.
- `invalidateTag("users")` borra todas las claves tagueadas `users` con
  `SMEMBERS` + `DEL`.

Recurso original: https://stackpractices.com/es/recipes/nodejs-caching-redis/
