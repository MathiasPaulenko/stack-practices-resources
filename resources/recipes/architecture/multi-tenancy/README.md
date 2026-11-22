# Multi-Tenancy — Companion Files

Runnable code for the recipe [Multi-Tenancy Architecture](https://stackpractices.com/recipes/multi-tenancy/).

## Files

- `tenant-isolation.sql` — PostgreSQL Row-Level Security DDL with `FORCE` and `missing_ok`.
- `tenant-middleware.js` — Express tenant resolution (`req.subdomains`) plus `withTenant`, a transaction-scoped `SET LOCAL` helper safe for pooled connections.
- `tenant-pool.ts` — per-tenant `pg.Pool` manager (module-level singleton, LRU-ready).
- `tenant_cache.py` — tenant-scoped Redis cache with `SCAN`-based invalidation.
- `migrate_tenant_schema.py` — schema-per-tenant migration helper (SQLAlchemy 2.x `text()`).
- `tenant-onboarding.ts` — onboarding/offboarding pipeline with sanitized identifiers.

## Requirements

- Node.js 18+, `npm install pg`
- Python 3.10+, `pip install redis sqlalchemy`
- PostgreSQL 12+ and a running Redis
