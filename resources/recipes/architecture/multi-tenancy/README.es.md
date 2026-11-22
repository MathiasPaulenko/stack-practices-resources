# Multi-tenancy — Archivos complementarios

Código ejecutable de la receta [Arquitectura Multi-Tenancy](https://stackpractices.com/es/recipes/multi-tenancy/).

## Archivos

- `tenant-isolation.sql` — DDL de Row-Level Security en PostgreSQL con `FORCE` y `missing_ok`.
- `tenant-middleware.js` — resolución de tenant en Express (`req.subdomains`) más `withTenant`, helper de `SET LOCAL` por transacción seguro con pools.
- `tenant-pool.ts` — gestor de `pg.Pool` por tenant (singleton a nivel de módulo, preparado para LRU).
- `tenant_cache.py` — caché Redis con scope de tenant e invalidación basada en `SCAN`.
- `migrate_tenant_schema.py` — helper de migración schema-por-tenant (`text()` de SQLAlchemy 2.x).
- `tenant-onboarding.ts` — pipeline de onboarding/offboarding con identificadores sanitizados.

## Requisitos

- Node.js 18+, `npm install pg`
- Python 3.10+, `pip install redis sqlalchemy`
- PostgreSQL 12+ y un Redis en ejecución
