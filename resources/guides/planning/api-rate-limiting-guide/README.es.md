# Rate Limiting de APIs — Recursos Complementarios

Implementaciones de rate limiting para la [guía de Rate Limiting](https://stackpractices.com/es/guides/api-rate-limiting-guide/).

| Archivo | Qué muestra |
|---------|-------------|
| `token_bucket.py` | Token bucket en proceso (ráfagas hasta la capacidad) |
| `sliding_window.py` | Ventana deslizante log (exacta) y counter (memoria O(1)) |
| `rate_limit.lua` | Token bucket atómico para Redis (`EVAL`) |
| `nginx_rate_limit.conf` | Límites a nivel gateway: zonas por IP y por API key |
| `fastapi_rate_limit.py` | FastAPI + `fastapi-limiter` con Redis |
