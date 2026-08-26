# optimistic-locking — Companion Resources

Companion code for [Optimistic Locking in Databases](https://stackpractices.com/recipes/optimistic-locking/).

## Files

| File | Language | Purpose |
|------|----------|---------|
| `optimistic_update.py` | Python | Single-row update with conflict detection |
| `optimistic_update.js` | JavaScript | Same in Node.js/Express with retry wrapper |
| `optimistic_update.java` | Java | JPA / Hibernate `@Version` example |
| `batch_update.py` | Python | Multi-row optimistic locking in one transaction |
| `etags.js` | JavaScript | ETag / If-Match HTTP optimistic locking |
| `README.md` / `README.es.md` | — | This doc |

## Requirements

- Python 3.10+ with `psycopg2-binary`
- Node.js 18+ with `pg` and `express`
- Java 17+ with Jakarta Persistence, Spring Data JPA
- PostgreSQL running locally or `DATABASE_URL` set

## Quick start

### Python

```bash
pip install psycopg2-binary
export DATABASE_URL="postgresql://user:pass@localhost/db"
python optimistic_update.py
```

### Node.js

```bash
npm install pg express
node optimistic_update.js
```

### Java

Compile and run the `ProductService` test in your Spring Boot project.

## Notes

- Create the `products` table with a `version` column:

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price NUMERIC,
    version INTEGER DEFAULT 0
);
```

- For production, add an index on `(id, version)`.
