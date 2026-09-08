"""Window function examples with PySpark."""
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window


def row_number_example(orders):
    """Rank orders by date within each customer."""
    window_spec = Window.partitionBy("customer_id").orderBy(F.desc("order_date"))
    return orders.withColumn("order_rank", F.row_number().over(window_spec))


def running_total_example(orders):
    """Running total per customer ordered by date."""
    running_window = (
        Window.partitionBy("customer_id")
        .orderBy("order_date")
        .rowsBetween(Window.unboundedPreceding, Window.currentRow)
    )
    return orders.withColumn("running_total", F.sum("amount").over(running_window))


def lag_example(orders):
    """Previous order amount per customer."""
    window_spec = Window.partitionBy("customer_id").orderBy(F.desc("order_date"))
    return orders.withColumn("prev_amount", F.lag("amount", 1).over(window_spec))


def percentile_example(orders):
    """Percentile within group."""
    return orders.withColumn(
        "amount_percentile",
        F.percent_rank().over(
            Window.partitionBy("category").orderBy("amount")
        ),
    )


if __name__ == "__main__":
    spark = SparkSession.builder.appName("window-functions").getOrCreate()
    data = [
        (1, "2025-01-15", 100.0, "electronics"),
        (1, "2025-01-20", 50.0, "books"),
        (2, "2025-01-15", 200.0, "electronics"),
        (2, "2025-02-01", 75.0, "books"),
    ]
    orders = spark.createDataFrame(data, ["customer_id", "order_date", "amount", "category"])
    row_number_example(orders).show()
    running_total_example(orders).show()
    lag_example(orders).show()
    spark.stop()
