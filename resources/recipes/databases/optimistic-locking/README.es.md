# optimistic-locking — Recursos complementarios

Código complementario para [Bloqueo optimista en bases de datos](https://stackpractices.com/es/recipes/optimistic-locking/).

## Archivos

| Archivo | Lenguaje | Propósito |
|---------|----------|-----------|
| `optimistic_update.py` | Python | Actualización de una fila con detección de conflicto |
| `optimistic_update.js` | JavaScript | Lo mismo en Node.js/Express con wrapper de reintento |
| `optimistic_update.java` | Java | Ejemplo JPA / Hibernate `@Version` |
| `batch_update.py` | Python | Bloqueo optimista de múltiples filas en una transacción |
| `etags.js` | JavaScript | Bloqueo optimista HTTP con ETag / If-Match |
| `README.md` / `README.es.md` | — | Esta documentación |

## Requisitos

- Python 3.10+ con `psycopg2-binary`
- Node.js 18+ con `pg` y `express`
- Java 17+ con Jakarta Persistence, Spring Data JPA
- PostgreSQL local o variable `DATABASE_URL`

## Inicio rápido

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

Compilar y ejecutar el test de `ProductService` en tu proyecto Spring Boot.

## Notas

- Crear la tabla `products` con columna `version`:

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price NUMERIC,
    version INTEGER DEFAULT 0
);
```

- En producción, agregar un índice sobre `(id, version)`.
