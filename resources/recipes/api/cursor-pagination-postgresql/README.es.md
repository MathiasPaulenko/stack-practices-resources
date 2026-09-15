# Paginación por Cursor en PostgreSQL (Keyset vs OFFSET)

Companion ejecutable para la receta de StackPractices en <https://stackpractices.com/recipes/cursor-pagination-postgresql/>.

## Archivos

| Archivo | Lenguaje | Descripción |
|---------|----------|-------------|
| `schema.sql` | SQL | Esquema de tabla, índices compuestos, índice parcial, columna generada |
| `cursor_pagination.ts` | TypeScript | Repositorio con driver `pg` y codificación de cursor base64url |
| `cursor_pagination.py` | Python | Implementación async con `asyncpg` |
| `CursorPagination.java` | Java | Implementación JDBC con `java.util.Base64` |

## Inicio rápido

```bash
# 1. Aplicar el esquema
psql -d tu_db -f schema.sql

# 2. TypeScript
npm install pg
npx tsx cursor_pagination.ts

# 3. Python
pip install asyncpg
python cursor_pagination.py

# 4. Java
javac CursorPagination.java
java -cp .:postgresql.jar CursorPagination
```

## Cómo funciona

1. El cliente solicita la primera página (sin cursor).
2. El servidor consulta `ORDER BY created_at DESC, id DESC LIMIT N+1`.
3. Si se retornan N+1 filas, `hasMore = true` y el siguiente cursor se codifica desde la fila N.
4. El cliente envía el cursor en la siguiente petición.
5. El servidor decodifica el cursor y consulta `WHERE (created_at, id) < (cursor_values)`.
6. La búsqueda en el índice es O(log n), por lo que las páginas profundas son tan rápidas como la primera.

## Índices clave

- `(created_at DESC, id DESC)` — ordenamiento estable con desempate.
- `(score DESC, id DESC)` — ordenamiento alternativo por puntuación.
- `WHERE deleted_at IS NULL` — índice parcial para filas eliminadas lógicamente.
