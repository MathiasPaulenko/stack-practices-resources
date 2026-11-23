# Invalidación de Caché Redis en Node.js

Companion ejecutable de la receta de StackPractices
[Implementar Invalidación de Caché Redis en Node.js](https://stackpractices.com/es/recipes/nodejs-redis-cache-invalidation/).

## Contenido

- **`cache.js`** — los helpers de invalidación de la receta en forma de librería: escritura con TTL (`cacheProduct`), `DEL` explícito + repoblado (`updateProduct`), limpieza por patrón `SCAN`+`DEL` con deduplicación y pipelines por lote (`invalidatePattern`), broadcast por pub/sub y suscriptor de la caché L1 (`publishInvalidation`, `createInvalidationSubscriber`), y bloqueo anti-estampida (`getProductWithLock`). El cliente de Redis se inyecta, así que el mismo código corre sobre `ioredis` o `ioredis-mock`.
- **`server.js`** — demo Express conectada a un Redis real en `localhost:6379`. Un mapa de productos en memoria hace de base de datos; un `Map` local hace de caché L1 que se mantiene sincronizada por el canal pub/sub `cache:invalidate`.
- **`test.js`** — suite `node:test` que corre end-to-end contra `ioredis-mock`. No hace falta servidor Redis: cubre escrituras con TTL, eliminación explícita, limpieza por patrón, propagación pub/sub a la L1 y el bloqueo.

## Ejecutar

```bash
npm install
npm test        # 4/4 tests contra ioredis-mock
npm start       # necesita un Redis real en localhost:6379
```

## Endpoints (con `npm start` corriendo)

| Ruta | Qué muestra |
|---|---|
| `GET /products/:id` | Lectura cache-aside L1 → Redis → DB con bloqueo anti-estampida |
| `PUT /products/:id` | Escritura write-through + broadcast de invalidación por pub/sub |
| `DELETE /products/:id` | Eliminación explícita + broadcast |
| `POST /invalidate-products` | Limpieza por patrón `SCAN`+`DEL` de todas las claves `product:*` |
| `GET /l1` | Contenido actual de la caché L1 en memoria |

Haz `PUT /products/1` con `{"price": 69}` dos veces seguidas y mira `GET /l1`:
el evento pub/sub limpia la entrada L1 entre llamada y llamada.
