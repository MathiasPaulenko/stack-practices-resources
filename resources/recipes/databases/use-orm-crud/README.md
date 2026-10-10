# ORM CRUD — SQLAlchemy, Prisma, Hibernate & Variants

Runnable CRUD examples for the same `User`/`Post` model across five ORMs.
Companion code for the StackPractices recipe:
<https://stackpractices.com/recipes/use-orm-crud/>

## Files

| File | Stack | What it shows |
|------|-------|---------------|
| `python_sqlalchemy_crud.py` | SQLAlchemy 2.x | `select()`/`session.scalar()` API, eager loading with `selectinload`, bulk operations |
| `javascript_prisma_crud.js` | Prisma | Nested creates, `$transaction`, `upsert`, parameterized `$queryRaw` |
| `schema.prisma` | Prisma | `User`/`Post` schema with indexes and relation |
| `java_jpa_crud.java` | Hibernate / JPA | `@Entity` mapping, `EntityManager` transactions |
| `django_orm_crud.py` | Django ORM | `prefetch_related`, `bulk_create`, aggregation with `annotate` |
| `typescript_typeorm_crud.ts` | TypeORM | Decorators, repository pattern, query-builder bulk update |
| `sql_schema.sql` | PostgreSQL | The schema the ORMs generate — useful as a reference |

## Quick start — Python (SQLAlchemy)

```bash
pip install -r requirements.txt
DATABASE_URL=sqlite:///orm_crud.db python python_sqlalchemy_crud.py
```

Any SQLAlchemy URL works: `postgresql+psycopg://user:pass@localhost/mydb` for Postgres.

## Quick start — JavaScript (Prisma)

```bash
npm install
npx prisma migrate dev --name init   # creates tables from schema.prisma
npm run crud:prisma
```

The bundled `schema.prisma` uses SQLite (`DATABASE_URL="file:./dev.db"`) so it runs without a database server. Switch `provider` to `postgresql` for a real deployment.

## Quick start — TypeScript (TypeORM)

```bash
npm install
npm run crud:typeorm
```

`synchronize: true` creates the tables automatically — fine for demos, use migrations in production.

## Java (Hibernate / JPA)

`java_jpa_crud.java` is a reference implementation: it needs a JPA provider and a
`persistence.xml` or Spring Boot autoconfiguration. Drop the entity and repository
into an existing project to use it.
