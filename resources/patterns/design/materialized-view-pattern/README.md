# Materialized View Pattern — Companion Resources

Code examples for the [Materialized View Pattern](https://stackpractices.com/patterns/materialized-view-pattern/) on StackPractices.

## Files

| File | Description |
|------|-------------|
| `mv_daily_revenue_django.py` | Django + Celery implementation: a plain table treated as a materialized view, with full and incremental refresh tasks and a read-only service layer. |
| `ProductStatsRefreshService.java` | Spring implementation: a JPA read entity plus an `@Scheduled` job that rebuilds the stats table nightly. |
| `materialized_views_postgres.sql` | PostgreSQL native materialized views: `CREATE MATERIALIZED VIEW`, `REFRESH` (full and `CONCURRENTLY`), and a trigger-based incremental refresh on a summary table. |

## Notes

- The Django example needs Celery configured (`celery beat` for scheduling). Adjust `orders_order` to your app's actual table name.
- `REFRESH MATERIALIZED VIEW CONCURRENTLY` requires a `UNIQUE` index on the view.
- The trigger example is intentionally minimal: it handles inserts. For updates and deletes, add matching trigger branches or reconcile with a periodic full refresh.
