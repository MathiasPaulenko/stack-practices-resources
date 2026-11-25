# Guía de Diseño de APIs REST — Recursos Complementarios

Snippets ejecutables de FastAPI que implementan las convenciones de la
[Guía de Diseño de APIs REST](https://stackpractices.com/es/guides/rest-api-design-guide/).

Cada archivo es autocontenido: instala `fastapi` y `uvicorn`, corre el archivo
con `uvicorn <modulo>:app` y pruébalo con `curl`.

## Archivos

| Archivo | Qué demuestra |
|---|---|
| `error_envelope.py` | Una forma de error consistente (`code`, `message`, `field`, `documentation_url`, `trace_id`) en todos los endpoints |
| `idempotency.py` | Manejo de `Idempotency-Key` en `POST /v1/orders`: replay guardado, 409 con body distinto |
| `etag_conditional.py` | `ETag` + `If-None-Match` → `304 Not Modified` en un `GET` |
| `rate_limit_headers.py` | Headers `X-RateLimit-*` y `429` + `Retry-After` |
| `deprecation.py` | Headers `Deprecation`, `Sunset` y `Link` en un endpoint deprecado |
| `cursor_pagination.py` | Paginación por cursor (`next_cursor`) en lugar de offset |
| `request_id.py` | Middleware `X-Request-ID` que devuelve el ID en cada respuesta |
| `openapi_snippet.yaml` | Fragmento de spec OpenAPI cubriendo los mismos endpoints |

## Inicio rápido

```bash
pip install fastapi uvicorn
uvicorn idempotency:app --port 8000

# el primer request guarda el resultado
curl -i -X POST localhost:8000/v1/orders \
  -H "Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"usr_123","items":[{"sku":"PROD-001","quantity":2}]}'

# reintentar con la misma key devuelve el 201 guardado, sin orden duplicada
```
