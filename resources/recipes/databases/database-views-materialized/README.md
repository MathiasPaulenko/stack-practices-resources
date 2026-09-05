# Database Views & Materialized Views — Companion

Runnable SQL examples for the StackPractices recipe
[Create and Use Database Views and Materialized Views](https://stackpractices.com/recipes/database-views-materialized/).

## Files

| File | Database | Description |
|------|----------|-------------|
| `postgresql_views.sql` | PostgreSQL | Regular views, materialized views, CONCURRENTLY refresh, access control |
| `sqlserver_indexed_view.sql` | SQL Server | SCHEMABINDING, clustered index, NOEXPAND |
| `mysql_simulated_mv.sql` | MySQL | Simulated materialized view with table + triggers |
| `pg_cron_schedule.sql` | PostgreSQL | Schedule refreshes with pg_cron |

## Quick start

### PostgreSQL

```bash
psql -d your_database -f postgresql_views.sql
psql -d your_database -f pg_cron_schedule.sql
```

### SQL Server

```bash
sqlcmd -S your_server -d your_database -i sqlserver_indexed_view.sql
```

### MySQL

```bash
mysql -u root -p your_database < mysql_simulated_mv.sql
```

## Source

- [Recipe (EN)](https://stackpractices.com/recipes/database-views-materialized/)
- [Recipe (ES)](https://stackpractices.com/es/recipes/database-views-materialized/)
