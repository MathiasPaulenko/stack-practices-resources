# Rate Limiting para Seguridad de APIs

Recursos de apoyo de la [receta Rate Limiting contra Abuso y Fuerza Bruta](https://stackpractices.com/es/recipes/rate-limiting-security/) en StackPractices.

Rate limiting como capa defensiva: token bucket atómico en Redis, middleware por niveles para Express, límites en el edge con Nginx y un script de prueba de ráfagas.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `token_bucket.lua` | Script Lua de comprobación y decremento atómico para Redis |
| `rate_limiter.py` | Caller en Python con helper de límite para login |
| `express_limiter.js` | Factory de middleware Express con límites por niveles (rate-limiter-flexible) |
| `nginx-rate-limit.conf` | Zonas `limit_req` de Nginx: estricta en `/api/auth/`, permisiva en `/api/` |
| `test_limits.sh` | Script que dispara una ráfaga y muestra cuándo aparece el 429 |

## Requisitos

- Redis 5+ local (`redis-server` o `docker run -p 6379:6379 redis`)
- Python: `pip install redis`
- Node.js: `npm install rate-limiter-flexible redis`

## Inicio rápido

```bash
# 1. Probar el limitador atómico directo en redis-cli
redis-cli --eval token_bucket.lua rl:test , 5 1 0 60

# 2. Ejemplo en Python — imprime allowed/limited por intento
python rate_limiter.py

# 3. Verificar un endpoint real
./test_limits.sh https://api.example.com/api/auth/login
```

## Notas

- Ejecuta siempre la comprobación y el decremento de forma atómica (Lua o una librería que lo haga internamente). El read/write en dos pasos deja pasar ráfagas con concurrencia.
- Usa como clave algo que el atacante no pueda rotar barato: `IP + cuenta` en auth, ID de usuario o API key en lecturas.
- Combínalo con tu WAF — el rate limiting frena a los atacantes, pero no los autentica.
