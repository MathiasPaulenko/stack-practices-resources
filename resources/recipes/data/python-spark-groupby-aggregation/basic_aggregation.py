"""Basic group-by aggregation examples with PySpark."""
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def build_spark() -> SparkSession:
    return (
        SparkSession.builder
        .appName("basic-aggregation")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .getOrCreate()
    )


def basic_groupby(spark: SparkSession, orders):
    """Sum, count, avg, max, min per customer."""
    return (
        orders.groupBy("customer_id")
        .agg(
            F.sum("amount").alias("total_spent"),
            F.count("order_id").alias("order_count"),
            F.avg("amount").alias("avg_order_value"),
            F.max("order_date").alias("last_order_date"),
            F.min("order_date").alias("first_order_date"),
        )
        .orderBy(F.desc("total_spent"))
    )


def groupby_multiple_columns(spark: SparkSession, orders):
    """Group by customer and month."""
    return (
        orders.groupBy(
            "customer_id",
            F.date_format("order_date", "yyyy-MM").alias("month"),
        )
        .agg(
            F.sum("amount").alias("monthly_spent"),
            F.countDistinct("order_id").alias("unique_orders"),
        )
        .orderBy("customer_id", "month")
    )


if __name__ == "__main__":
    spark = build_spark()
    data = [
        (1, "2025-01-15", 100.0, "completed"),
        (1, "2025-01-20", 50.0, "completed"),
        (2, "2025-01-15", 200.0, "cancelled"),
        (2, "2025-02-01", 75.0, "completed"),
        (3, "2025-01-10", 300.0, "completed"),
    ]
    orders = spark.createDataFrame(data, ["customer_id", "order_date", "amount", "status"])
    result = basic_groupby(spark, orders)
    result.show()
    spark.stop()
