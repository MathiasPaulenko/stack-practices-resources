# Rate Limiting de APIs — Recursos Companion

Companion ejecutable de la receta **[Rate Limiting de APIs](https://stackpractices.com/es/recipes/api-rate-limiting/)** en StackPractices.

## Archivos

| Archivo | Propósito |
|---|---|
| `token_bucket.lua` | Token bucket atómico para Redis — la lectura-check-actualización corre dentro de Redis, así que las peticiones concurrentes no pueden competir por el contador (la debilidad de `hgetall` + `hset` en código de aplicación). |
| `rate_limiter.py` | Wrapper de Python: `RateLimiter.token_bucket()` (respaldado por Lua, atómico), `RateLimiter.sliding_window()` (sorted set) y `token_bucket_fail_open()` para tolerancia a Redis caído. |
| `express-rate-limit.js` | Middleware de Express: sliding window con key por API key → user ID → IP, 429s con problem+json RFC 9457, headers `X-RateLimit-*`, fail-open ante errores de Redis. |
| `test_rate_limiter.py` | Suite pytest que cubre los cuatro escenarios de la receta: enforcement (N+1), reset de ventana, failover de Redis y consistencia distribuida. |

## Inicio rápido — Python

```bash
pip install redis fakeredis pytest
docker run -d -p 6379:6379 redis:7   # o sáltalo y deja que fakeredis cubra los tests
pytest test_rate_limiter.py -v
```

```python
import redis
from rate_limiter import RateLimiter

limiter = RateLimiter(redis.Redis(host='localhost', port=6379))
result = limiter.token_bucket("user:u_4812", capacity=100, refill_rate=1.6)
if not result.allowed:
    return {"error": "rate limited", "retry_after": result.retry_after}, 429
```

## Inicio rápido — Express

```bash
npm install express redis
node -e "
const express = require('express');
const { rateLimit } = require('./express-rate-limit');
const app = express();
app.use((req, res, next) => { req.id = 'req_demo'; next(); });
app.use(rateLimit({ limit: 5, windowSec: 60 }));
app.get('/ping', (req, res) => res.json({ ok: true }));
app.listen(3000);
" &
for i in 1 2 3 4 5 6 7; do curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/ping; done
# 200 ×5, luego 429 con application/problem+json + Retry-After
```

## Notas

- `REDIS_URL` sobrescribe el `redis://localhost:6379` por defecto en el middleware.
- El script Lua toma `now` como argumento — pasa el reloj del llamador, no `TIME`, para que los tests puedan controlar el tiempo.
- `token_bucket_fail_open` es la política deliberada: un limiter muerto permite el tráfico y loguea, no tira la API. Invértelo (fail closed) solo donde el acceso ilimitado es peor que el downtime.
