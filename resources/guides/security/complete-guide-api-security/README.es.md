# Seguridad de APIs — Companion

Controles de seguridad ejecutables de la [Guía Completa de Seguridad de APIs](https://stackpractices.com/es/guides/complete-guide-api-security/).

## Archivos

- `token_bucket_limiter.py` — rate limiter token-bucket en memoria + middleware FastAPI
- `redis_rate_limiter.py` — limiter sliding-window sobre sorted sets de Redis
- `tiered_limiter.py` — límites por plan (free/pro/enterprise)
- `pydantic_validation.py` — validación por esquema con Pydantic v2 (Field, field_validator)
- `file_upload_validation.py` — comprobación de MIME por magic bytes + nombres seguros
- `cors_config.py` — CORS estricto
- `sql_injection_prevention.py` — patrones vulnerables vs seguros + listas blancas
- `mass_assignment_protection.py` — esquemas de update explícitos, model_dump
- `gateway_middleware.py` — límites de tamaño, API keys, rate limits, security headers
- `pagination_security.py` — topes de página + cursor pagination endurecida
- `audit_logging.py` — audit log estructurado + eventos de seguridad
- `test_api_security.py` — suite pytest: inyección, mass assignment, CORS, auth, paginación

## Uso

Requiere `fastapi`, `pydantic>=2`, `redis`, `python-magic`, `pytest`, `httpx`. Copia lo que necesites; corre tests con `pytest test_api_security.py` contra tus fixtures.
