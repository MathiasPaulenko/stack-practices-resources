# Seed Database — Companion Resources

Runnable seeding examples matching the [Seed Database](https://stackpractices.com/recipes/seed-database/) recipe.

## Contents

| File | Stack |
|------|-------|
| `db/seeds/*.sql` | PostgreSQL seed files (ordered, idempotent via `ON CONFLICT`) |
| `db/seed.js` | Node.js `pg` runner — executes `db/seeds/` in a transaction |
| `seeds/mongo-seed.js` | MongoDB seed with `deleteMany` + `insertMany` + index creation |
| `prisma/seed.ts` | Prisma seed with `upsert` (run via `npx prisma db seed`) |
| `scripts/seed_database.py` | SQLAlchemy seed script with production guard |

## Usage

```bash
# PostgreSQL (requires `pg` package and DATABASE_URL)
node db/seed.js

# MongoDB (requires `mongodb` package and MONGODB_URI)
node seeds/mongo-seed.js

# Prisma (requires prisma + ts-node)
npx prisma db seed

# SQLAlchemy
python scripts/seed_database.py
```

All scripts are idempotent and refuse to run when `NODE_ENV=production` / `ENV=production`. Never seed production with test data — use controlled migrations for reference data only.
