# Multi-Tenant Data Isolation Pattern

Runnable examples for the three tenant-isolation strategies described in the
[StackPractices pattern](https://stackpractices.com/patterns/multi-tenant-data-isolation-pattern/):

| File | Strategy | Notes |
|---|---|---|
| `src/row_level_security.py` | RLS (shared schema) | `FORCE ROW LEVEL SECURITY` + `set_config(..., true)` scoped to the transaction |
| `src/schema_per_tenant.py` | Schema-per-tenant | Sanitized schema names; `create_all` runs on the connection with `search_path` set |
| `src/database_per_tenant.js` | Database-per-tenant | One `pg.Pool` per tenant database |
| `src/TenantInterceptor.java` | Tenant resolution | Spring `HandlerInterceptor` extracting `X-Tenant-ID` |
| `src/TenantContext.java` | Tenant context | `ThreadLocal` holder (own file in a real project) |
| `src/DocumentRepository.java` | Repository | Schema name validated before interpolation |

## Requirements

- Python 3.10+ with SQLAlchemy 2.x and psycopg2
- Node.js 18+ with `pg`
- Java 17+ with Spring MVC (examples are illustrative snippets)

## Notes

- The Python examples target PostgreSQL — RLS and `search_path` are Postgres-specific.
- Never interpolate raw tenant identifiers into SQL/DDL. The examples sanitize or whitelist first.
- Session-level `SET` on pooled connections leaks tenant context; always scope it to the transaction.
