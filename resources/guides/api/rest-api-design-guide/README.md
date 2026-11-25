# REST API Design Guide — Companion Resources

Runnable FastAPI snippets that implement the conventions from the
[REST API Design Guide](https://stackpractices.com/guides/rest-api-design-guide/).

Each file is self-contained: install `fastapi` and `uvicorn`, run the file
with `uvicorn <module>:app`, and hit it with `curl`.

## Files

| File | What it demonstrates |
|---|---|
| `error_envelope.py` | One consistent error shape (`code`, `message`, `field`, `documentation_url`, `trace_id`) across every endpoint |
| `idempotency.py` | `Idempotency-Key` handling on `POST /v1/orders`: stored replay, 409 on body mismatch |
| `etag_conditional.py` | `ETag` + `If-None-Match` → `304 Not Modified` on a `GET` |
| `rate_limit_headers.py` | `X-RateLimit-*` headers and `429` + `Retry-After` |
| `deprecation.py` | `Deprecation`, `Sunset` and `Link` headers on a deprecated endpoint |
| `cursor_pagination.py` | Cursor pagination (`next_cursor`) instead of offset |
| `request_id.py` | `X-Request-ID` middleware echoing the ID on every response |
| `openapi_snippet.yaml` | OpenAPI spec fragment covering the same endpoints |

## Quick start

```bash
pip install fastapi uvicorn
uvicorn idempotency:app --port 8000

# first request stores the result
curl -i -X POST localhost:8000/v1/orders \
  -H "Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"usr_123","items":[{"sku":"PROD-001","quantity":2}]}'

# retry with the same key returns the stored 201, no duplicate order
```
