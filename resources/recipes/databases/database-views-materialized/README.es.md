# Vistas de Base de Datos & Vistas Materializadas — Companion

Ejemplos SQL ejecutables para la receta de StackPractices
[Crear y usar vistas y vistas materializadas](https://stackpractices.com/es/recipes/database-views-materialized/).

## Archivos

| Archivo | Base de datos | Descripción |
|---------|---------------|-------------|
| `postgresql_views.sql` | PostgreSQL | Vistas regulares, vistas materializadas, refresh CONCURRENTLY, control de acceso |
| `sqlserver_indexed_view.sql` | SQL Server | SCHEMABINDING, clustered index, NOEXPAND |
| `mysql_simulated_mv.sql` | MySQL | Vista materializada simulada con tabla + triggers |
| `pg_cron_schedule.sql` | PostgreSQL | Programar refreshes con pg_cron |

## Inicio rápido

### PostgreSQL

```bash
psql -d tu_database -f postgresql_views.sql
psql -d tu_database -f pg_cron_schedule.sql
```

### SQL Server

```bash
sqlcmd -S tu_server -d tu_database -i sqlserver_indexed_view.sql
```

### MySQL

```bash
mysql -u root -p tu_database < mysql_simulated_mv.sql
```

## Fuente

- [Receta (EN)](https://stackpractices.com/recipes/database-views-materialized/)
- [Receta (ES)](https://stackpractices.com/es/recipes/database-views-materialized/)
