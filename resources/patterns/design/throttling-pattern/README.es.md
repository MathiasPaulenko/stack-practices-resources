# Patrón de Throttling — Ejemplos ejecutables

Archivos complementarios del [Patrón de Throttling](https://stackpractices.com/es/patterns/throttling-pattern/):

- `token_bucket.py` — token bucket en Python con `threading.Lock`, usado por el wrapper `ThrottledAPI`
- `ThrottledService.java` — servicio Spring con `RateLimiter` de Guava y `tryAcquire()`
- `sliding_window.js` — throttle de ventana deslizante por cliente
- `throttle.ts` — cliente auto-limitado para una API de terceros (espera el siguiente hueco)
- `token_bucket.lua` — token bucket atómico para Redis, para despliegues multi-instancia

Los archivos Python y JavaScript corren tal cual. El script Lua va por `EVAL`/`EVALSHA` contra Redis: `KEYS[1]` conteo de tokens, `KEYS[2]` timestamp del último refill, `ARGV` = capacidad, timestamp base, ahora, tasa.
