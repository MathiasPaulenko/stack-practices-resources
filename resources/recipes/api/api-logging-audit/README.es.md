# Logging y audit trails de API — Ejemplos de middleware

Compañero de la receta de StackPractices [Implementar logging y audit trails de API](https://stackpractices.com/es/recipes/api-logging-audit/).

Tres middlewares de auditoría equivalentes. Cada uno:

- Asigna o respeta `X-Correlation-Id` y lo devuelve en la respuesta.
- Emite una entrada de auditoría JSON estructurada por petición (timestamp en UTC, método, path, status, IP de cliente, user agent).
- Mantiene la escritura de auditoría fuera del camino crítico (logger rápido / transporte async).

## Archivos

| Archivo | Stack | Ejecutar |
| --- | --- | --- |
| `src/audit_middleware.py` | FastAPI + Uvicorn | `uvicorn src.audit_middleware:app` |
| `src/audit-middleware.js` | Express + Winston | `node src/audit-middleware.js` (requiere `express winston uuid`) |
| `src/AuditFilter.java` | Spring Boot + SLF4J/Logback | incluir en una app Spring Boot |

## Pruébalo

```bash
curl -i http://127.0.0.1:3000/health   # o :8000 para FastAPI
# La respuesta incluye: X-Correlation-Id: <uuid>
# Línea de log: {"timestamp": "...", "correlation_id": "...", ...}
```

Las entradas de auditoría (quién hizo qué, cuándo, desde dónde) van a almacenamiento append-only — el sink del logger es solo el transporte.
