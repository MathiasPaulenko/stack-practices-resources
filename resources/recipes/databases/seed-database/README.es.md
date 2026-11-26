# Seed de la Base de Datos — Recursos Complementarios

Ejemplos ejecutables de seed correspondientes a la receta [Seed Database](https://stackpractices.com/es/recipes/seed-database/).

## Contenido

| Archivo | Stack |
|---------|-------|
| `db/seeds/*.sql` | Archivos de seed PostgreSQL (ordenados, idempotentes vía `ON CONFLICT`) |
| `db/seed.js` | Runner Node.js `pg` — ejecuta `db/seeds/` en una transacción |
| `seeds/mongo-seed.js` | Seed de MongoDB con `deleteMany` + `insertMany` + creación de índices |
| `prisma/seed.ts` | Seed de Prisma con `upsert` (vía `npx prisma db seed`) |
| `scripts/seed_database.py` | Script de seed SQLAlchemy con protección de producción |

Todos los scripts son idempotentes y se niegan a ejecutarse con `NODE_ENV=production` / `ENV=production`.
