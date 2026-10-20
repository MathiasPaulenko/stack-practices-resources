# Checklist de Optimización de Consultas — Pack SQL de Triage

Recursos companion del doc [Checklist de Optimización de Consultas SQL](https://stackpractices.com/es/docs/database-query-tuning-checklist/).

## Archivos

| Archivo | Qué es |
| --- | --- |
| `top-slow-queries.sql` | Informes de `pg_stat_statements`: top consultas por tiempo total y peor ratio de caché; activación del slow log; equivalente MySQL `performance_schema` |
| `index-audit.sql` | Auditoría de salud de índices: uso por tabla, índices sin uso, tablas con seq scans pesados, consulta de selectividad, detección de índices duplicados |

## Uso

```bash
# PostgreSQL — ejecútalo en psql contra la base de datos objetivo
psql -d mydb -f top-slow-queries.sql
psql -d mydb -f index-audit.sql

# Instala la extensión una vez (si pg_stat_statements da error)
# CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

## Trampas

- `pg_stat_statements` se resetea al reiniciar — ejecuta los informes antes de reiniciar o guárdalos.
- `idx_scan = 0` no siempre significa "borrable": revisa constraints únicos (`indisunique`) e índices usados solo en ventanas batch.
- Nunca dejes `long_query_time = 0` / `log_min_duration_statement = 0` encendidos en producción — inundación de logs.
