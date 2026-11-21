"""Materialized view implemented as a plain table refreshed by Celery tasks.

Companion code for https://stackpractices.com/patterns/materialized-view-pattern/
Requires Django + Celery. Adjust model/table names to your schema.
"""
import logging

from celery import shared_task
from django.db import models, connection

logger = logging.getLogger(__name__)


# Source models
class Order(models.Model):
    customer_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


# Materialized view model
class DailyRevenueView(models.Model):
    date = models.DateField(primary_key=True)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    order_count = models.IntegerField()
    last_refreshed = models.DateTimeField()

    class Meta:
        managed = False  # Django doesn't manage this table
        db_table = "mv_daily_revenue"


@shared_task
def refresh_daily_revenue_view() -> None:
    """Complete rebuild of the materialized view."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DROP TABLE IF EXISTS mv_daily_revenue;
            CREATE TABLE mv_daily_revenue AS
            SELECT
                DATE(created_at) as date,
                SUM(amount) as total_revenue,
                COUNT(*) as order_count,
                NOW() as last_refreshed
            FROM orders_order
            WHERE status = 'completed'
            GROUP BY DATE(created_at);
            CREATE INDEX idx_mv_date ON mv_daily_revenue(date);
            """
        )
    logger.info("Daily revenue materialized view refreshed")


@shared_task
def incremental_refresh_daily_revenue() -> None:
    """Only update rows affected since the last refresh."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(date) FROM mv_daily_revenue")
        last_date = cursor.fetchone()[0]

        if last_date:
            cursor.execute(
                """
                DELETE FROM mv_daily_revenue
                WHERE date >= %s;
                """,
                [last_date],
            )

            cursor.execute(
                """
                INSERT INTO mv_daily_revenue
                SELECT
                    DATE(created_at) as date,
                    SUM(amount) as total_revenue,
                    COUNT(*) as order_count,
                    NOW() as last_refreshed
                FROM orders_order
                WHERE status = 'completed'
                  AND DATE(created_at) >= %s
                GROUP BY DATE(created_at);
                """,
                [last_date],
            )
        else:
            refresh_daily_revenue_view.delay()

    logger.info("Incremental refresh completed")


class RevenueService:
    """Read side: queries hit the materialized view, never the source table."""

    def get_revenue_for_date(self, date):
        try:
            return DailyRevenueView.objects.get(date=date)
        except DailyRevenueView.DoesNotExist:
            return None

    def get_revenue_range(self, start_date, end_date):
        return DailyRevenueView.objects.filter(
            date__range=(start_date, end_date)
        ).order_by("date")
