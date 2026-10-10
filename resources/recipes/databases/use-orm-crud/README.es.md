# CRUD con ORM — SQLAlchemy, Prisma, Hibernate y variantes

Ejemplos CRUD ejecutables del mismo modelo `User`/`Post` en cinco ORMs.
Código complementario de la receta de StackPractices:
<https://stackpractices.com/es/recipes/use-orm-crud/>

## Archivos

| Archivo | Stack | Qué muestra |
|---------|-------|-------------|
| `python_sqlalchemy_crud.py` | SQLAlchemy 2.x | API `select()`/`session.scalar()`, carga anticipada con `selectinload`, operaciones masivas |
| `javascript_prisma_crud.js` | Prisma | Creaciones anidadas, `$transaction`, `upsert`, `$queryRaw` parametrizado |
| `schema.prisma` | Prisma | Esquema `User`/`Post` con índices y relación |
| `java_jpa_crud.java` | Hibernate / JPA | Mapeo con `@Entity`, transacciones con `EntityManager` |
| `django_orm_crud.py` | Django ORM | `prefetch_related`, `bulk_create`, agregación con `annotate` |
| `typescript_typeorm_crud.ts` | TypeORM | Decoradores, patrón repositorio, actualización masiva con query builder |
| `sql_schema.sql` | PostgreSQL | El esquema que generan los ORMs — útil como referencia |

## Inicio rápido — Python (SQLAlchemy)

```bash
pip install -r requirements.txt
DATABASE_URL=sqlite:///orm_crud.db python python_sqlalchemy_crud.py
```

Vale cualquier URL de SQLAlchemy: `postgresql+psycopg://user:pass@localhost/mydb` para Postgres.

## Inicio rápido — JavaScript (Prisma)

```bash
npm install
npx prisma migrate dev --name init   # crea las tablas desde schema.prisma
npm run crud:prisma
```

El `schema.prisma` incluido usa SQLite (`DATABASE_URL="file:./dev.db"`) para funcionar sin servidor de base de datos. Cambia `provider` a `postgresql` en un despliegue real.

## Inicio rápido — TypeScript (TypeORM)

```bash
npm install
npm run crud:typeorm
```

`synchronize: true` crea las tablas automáticamente — bien para demos, pero en producción usa migraciones.

## Java (Hibernate / JPA)

`java_jpa_crud.java` es una implementación de referencia: necesita un proveedor JPA
y un `persistence.xml` o la autoconfiguración de Spring Boot. Copia la entidad y el
repositorio en un proyecto existente para usarlo.
