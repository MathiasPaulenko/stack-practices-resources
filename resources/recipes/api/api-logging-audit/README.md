# API Logging and Audit Trails — Middleware Examples

Companion to the StackPractices recipe [Implement API Logging and Audit Trails](https://stackpractices.com/recipes/api-logging-audit/).

Three equivalent audit middlewares. Each one:

- Assigns or honors `X-Correlation-Id` and echoes it in the response.
- Emits one structured JSON audit entry per request (timestamp in UTC, method, path, status, client IP, user agent).
- Keeps the audit write off the critical path (fast logger.info / async transport).

## Files

| File | Stack | Run |
| --- | --- | --- |
| `src/audit_middleware.py` | FastAPI + Uvicorn | `uvicorn src.audit_middleware:app` |
| `src/audit-middleware.js` | Express + Winston | `node src/audit-middleware.js` (needs `express winston uuid`) |
| `src/AuditFilter.java` | Spring Boot + SLF4J/Logback | drop into a Spring Boot app |

## Try it

```bash
curl -i http://127.0.0.1:3000/health   # or :8000 for FastAPI
# Response includes: X-Correlation-Id: <uuid>
# Log line: {"timestamp": "...", "correlation_id": "...", ...}
```

Audit entries (who did what, when, from where) belong in append-only storage — the logger sink is just the transport.
