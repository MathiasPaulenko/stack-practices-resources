# Indexación de bases de datos — Código complementario

SQL ejecutable que acompaña a la [receta de indexación de bases de datos](https://stackpractices.com/es/recipes/database-indexing/) en StackPractices.

## Archivos

| Archivo | Contenido |
|---------|-----------|
| `schema.sql` | Tablas de demo `users` y `orders` |
| `indexes.sql` | Los siete tipos de índice de la receta: una columna, compuesto, parcial, covering (INCLUDE), de expresión, FK y cursor por clave |
| `queries.sql` | Consultas `EXPLAIN ANALYZE` que ejercitan cada índice, más queries de mantenimiento (índices sin uso, FK sin indexar, ratio HOT) |

## Ejecutarlo

```bash
psql -d tu_db -f schema.sql
psql -d tu_db -f indexes.sql
# Carga algunas filas, y después:
psql -d tu_db -f queries.sql
```

Se recomienda PostgreSQL 14+ — `INCLUDE`, las columnas generadas y utilidades tipo `hypopg` lo requieren. Las queries de mantenimiento del final de `queries.sql` son específicas de PostgreSQL; el resto porta a MySQL 8 con cambios menores de sintaxis (`EXPLAIN ANALYZE` en lugar de `EXPLAIN (ANALYZE, BUFFERS)`).

## Qué observar

- `Seq Scan` vs `Index Scan` vs `Index Only Scan` en los planes
- `Heap Fetches: 0` en la query 5 — el índice covering respondiendo entero
- El cambio de plan en la query 4 al quitar `deleted_at IS NULL` del predicado
