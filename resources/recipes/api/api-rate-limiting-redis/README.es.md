# Rate Limiting de APIs con Redis — Recursos Companion

Companion ejecutable de la receta **[Implementar Rate Limiting de APIs con Redis](https://stackpractices.com/es/recipes/api-rate-limiting-redis/)** en StackPractices.

## Archivos

| Archivo | Propósito |
|---|---|
| `TokenBucket.ts` | Token bucket atómico para Redis. El cálculo del refill corre dentro de un script Lua y el tiempo viene de `redis.call('TIME')`, así que cada nodo mide contra el mismo reloj — sin deriva entre instancias. |
| `SlidingWindow.ts` | Contador de ventana deslizante sobre un sorted set de Redis (`ZADD`/`ZREMRANGEBYSCORE`/`ZCARD` en un solo pipeline). Más estricto que token bucket: registra los timestamps exactos de cada petición. |
| `rateLimit.ts` | Middleware de Express que emite headers `RateLimit-*` del IETF en cada respuesta y `429` + `Retry-After` cuando el bucket se vacía. |
| `TierConfig.ts` | Configuración por tier de usuario: buckets `free`/`pro`/`enterprise` con su propia capacidad y refill rate, con keys `rate:{tier}:{userId}`. |

## Inicio rápido

```bash
npm install express ioredis
docker run -d -p 6379:6379 redis:7
```

```typescript
import express from 'express';
import { Redis } from 'ioredis';
import { TokenBucketLimiter } from './TokenBucket';
import { rateLimit } from './rateLimit';

const app = express();
const limiter = new TokenBucketLimiter(new Redis());

app.use('/api/public', rateLimit(limiter, { capacity: 100, refillRate: 10 }));
app.use('/api/premium', rateLimit(limiter, { capacity: 1000, refillRate: 100 }));
app.listen(3000);
```

## Comprueba que funciona

Lanza peticiones hasta vaciar el bucket y verás que la 11ª devuelve `429` con `Retry-After`:

```bash
for i in $(seq 1 11); do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/api/public; done
```

## Notas de producción

- Envuelve las llamadas a Redis en un circuit breaker y falla abierto — una caída de Redis no debería convertirse en una caída de la API.
- Todo comando mutador debe establecer `EXPIRE`/`PEXPIRE`, o los clientes inactivos mantienen las keys vivas para siempre.
- En Redis Cluster, usa hash tags (`rate:{tenantId}:…`) para que las keys de cada cliente caigan en el mismo slot.
