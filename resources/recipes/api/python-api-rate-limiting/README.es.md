# Rate Limiting de API en Python — Companion

Companion ejecutable de la recipe de StackPractices: un `TokenBucket` en memoria, una app Flask mínima que lo aplica por IP con header `Retry-After`, y cobertura pytest para ráfagas, recarga, rechazos y el cálculo de `retry_after`.

## Archivos

- `token_bucket.py` — el limitador. Ejecuta `python token_bucket.py` para una demo rápida.
- `flask_app.py` — app Flask que aplica el cubo por IP de cliente. `python flask_app.py` y llama a `/api/data` más de 11 veces.
- `test_token_bucket.py` — 7 tests. `pytest test_token_bucket.py` (los tests unitarios no necesitan Redis ni Flask).

## Notas

Los cubos en memoria son por proceso — usa la variante con Redis y Lua de la recipe cuando ejecutes más de una instancia.

## Fuente

- [Python API Rate Limiting with Token Bucket — StackPractices](https://stackpractices.com/recipes/python-api-rate-limiting/)
- [Rate Limiting de API en Python — StackPractices](https://stackpractices.com/es/recipes/python-api-rate-limiting/)
