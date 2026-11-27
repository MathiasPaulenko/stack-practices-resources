# Encontrar y eliminar filas duplicadas en SQL

Scripts SQL ejecutables para detectar y eliminar filas duplicadas de forma segura. Los scripts de detección funcionan en cualquier motor; las variantes de borrado están agrupadas por técnica y motor. Ejecuta siempre la previsualización con `SELECT` antes de cualquier `DELETE`, y lanza las limpiezas dentro de una transacción o en una ventana de mantenimiento en producción.

## Archivos

| Archivo | Motor | Qué muestra |
|---------|-------|-------------|
| `find-duplicates.sql` | Cualquiera | Detección con `GROUP BY` + `HAVING`, claves multi-columna, coincidencia insensible a mayúsculas y sobre JSONB |
| `delete-duplicates-window-functions.sql` | PostgreSQL, MySQL 8+, SQLite 3.25+, SQL Server | CTE de previsualización, borrado transaccional con backup, verificación, restricción única |
| `delete-duplicates-mysql57.sql` | MySQL 5.7 | Borrado con self-join conservando `MIN(id)` — sin window functions |
| `batch-delete-duplicates.sql` | PostgreSQL | Bucle `DO $$` que borra en lotes de 1000 con `pg_sleep`, más `ANALYZE`/`REINDEX`/`VACUUM FULL` |
| `merge-duplicates-before-delete.sql` | PostgreSQL | Fusión de valores no nulos en la fila canónica antes de borrar |
| `case-insensitive-dedup.sql` | PostgreSQL | Particionado por `LOWER(email)` más índice único funcional para evitar recurrencia |
| `dedup-across-tables.sql` | Cualquiera | Detección con `UNION ALL` entre `users` y `archived_users`, limpieza del archivo |
| `clean-table-swap.sql` | PostgreSQL | Copia limpia con `DISTINCT ON` + intercambio atómico para tablas muy duplicadas |

## Uso

Prueba los scripts primero contra una copia de tus datos:

```sql
CREATE TABLE users_dedup_test AS SELECT * FROM users;
```

Luego adapta las columnas de `PARTITION BY` (la "clave de unicidad") y el `ORDER BY` (qué fila conservar) a tu esquema.

## Punto clave

El `ORDER BY` dentro de `ROW_NUMBER() OVER (...)` decide qué fila sobrevive — la más antigua, la más reciente, la más completa o la de mayor id. Elígelo con lógica de negocio, no al azar, y añade una restricción única después para que los duplicados no vuelvan.

Fuente: https://stackpractices.com/recipes/sql-find-duplicate-rows/
