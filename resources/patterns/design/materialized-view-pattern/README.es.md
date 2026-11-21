# Patrón de Vista Materializada — Recursos complementarios

Ejemplos de código para el [Patrón de Vista Materializada](https://stackpractices.com/es/patterns/materialized-view-pattern/) en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `mv_daily_revenue_django.py` | Implementación con Django + Celery: una tabla normal usada como vista materializada, con tareas de refresco completo e incremental y una capa de servicio de solo lectura. |
| `ProductStatsRefreshService.java` | Implementación con Spring: una entidad JPA de lectura más un job `@Scheduled` que reconstruye la tabla de estadísticas cada noche. |
| `materialized_views_postgres.sql` | Vistas materializadas nativas de PostgreSQL: `CREATE MATERIALIZED VIEW`, `REFRESH` (completo y `CONCURRENTLY`) y un refresco incremental por trigger sobre una tabla de resumen. |

## Notas

- El ejemplo de Django necesita Celery configurado (`celery beat` para la programación). Ajusta `orders_order` al nombre real de la tabla en tu app.
- `REFRESH MATERIALIZED VIEW CONCURRENTLY` exige un índice `UNIQUE` sobre la vista.
- El ejemplo de trigger es mínimo a propósito: solo maneja inserts. Para updates y deletes, añade ramas de trigger equivalentes o reconcilia con un refresco completo periódico.
