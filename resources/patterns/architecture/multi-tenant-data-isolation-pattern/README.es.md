# Patrón Multi-Tenant Data Isolation

Ejemplos ejecutables de las tres estrategias de aislamiento de tenants descritas en el
[patrón de StackPractices](https://stackpractices.com/es/patterns/multi-tenant-data-isolation-pattern/):

| File | Strategy | Notes |
|---|---|---|
| `src/row_level_security.py` | RLS (shared schema) | `FORCE ROW LEVEL SECURITY` + `set_config(..., true)` scoped to the transaction |
| `src/schema_per_tenant.py` | Schema-per-tenant | Sanitized schema names; `create_all` runs on the connection with `search_path` set |
| `src/database_per_tenant.js` | Database-per-tenant | One `pg.Pool` per tenant database |
| `src/TenantInterceptor.java` | Tenant resolution | Spring `HandlerInterceptor` extracting `X-Tenant-ID` |
| `src/TenantContext.java` | Tenant context | `ThreadLocal` holder (own file in a real project) |
| `src/DocumentRepository.java` | Repository | Schema name validated before interpolation |

## Requisitos

- Python 3.10+ con SQLAlchemy 2.x y psycopg2
- Node.js 18+ con `pg`
- Java 17+ con Spring MVC (los ejemplos son fragmentos ilustrativos)

## Notas

- Los ejemplos de Python usan PostgreSQL — RLS y `search_path` son específicos de Postgres.
- Nunca interpola identificadores de tenant en crudo en SQL/DDL. Los ejemplos los sanitizan o validan primero.
- Un `SET` a nivel de sesión en conexiones compartidas filtra el contexto del tenant; limítalo siempre a la transacción.
