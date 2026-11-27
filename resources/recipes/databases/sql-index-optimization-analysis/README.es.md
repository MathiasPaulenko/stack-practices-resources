# Analizar y optimizar índices SQL — Scripts de apoyo

Scripts ejecutables de PostgreSQL que acompañan la receta
[Analizar y optimizar índices SQL con EXPLAIN](https://stackpractices.com/es/recipes/sql-index-optimization-analysis/).

## Archivos

| Script | Qué hace |
|--------|----------|
| `explain-analyze-baseline.sql` | EXPLAIN ANALYZE de referencia + índice compuesto para una consulta lenta |
| `find-unused-indexes.sql` | Índices sin escaneos, con tamaños |
| `find-duplicate-indexes.sql` | Índices que cubren columnas idénticas |
| `partial-index.sql` | Índice parcial solo sobre filas activas |
| `covering-index.sql` | Índice INCLUDE para Index Only Scans |
| `expression-index.sql` | Índices sobre `LOWER(email)` y `DATE_TRUNC` |
| `drop-index-safely.sql` | Revisión de tamaño + `DROP INDEX CONCURRENTLY` |
| `reindex-and-analyze.sql` | REINDEX CONCURRENTLY + refresco de estadísticas |
| `monitoring-weekly.sql` | Consultas semanales de salud de índices para cron |
| `hypothetical-index-hypopg.sql` | Probar el impacto de un índice con HypoPG |

## Uso

Requiere PostgreSQL 11+ (`INCLUDE` y `REINDEX CONCURRENTLY` necesitan PG11+/12+).
`hypothetical-index-hypopg.sql` necesita la extensión [HypoPG](https://hypopg.readthedocs.io/).

```bash
psql -d tu_db -f explain-analyze-baseline.sql
```

Todos los scripts de drop/reindex usan `CONCURRENTLY`, así que son seguros en
tablas en vivo, pero monitorea el uso de índices al menos una semana antes
de eliminar nada en producción.

## Más recursos

- Receta (EN): https://stackpractices.com/recipes/sql-index-optimization-analys
