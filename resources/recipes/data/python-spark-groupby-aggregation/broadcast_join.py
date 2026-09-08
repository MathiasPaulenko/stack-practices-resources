"""Broadcast join example with PySpark."""
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def broadcast_join(orders, customers):
    """Broadcast small dimension table to avoid shuffle."""
    return orders.join(
        F.broadcast(customers),
        on="customer_id",
        how="left",
    )


def regular_join(orders, customers):
    """Regular join triggers shuffle (slow for large tables)."""
    return orders.join(customers, on="customer_id", how="left")


if __name__ == "__main__":
    spark = SparkSession.builder.appName("broadcast-join").getOrCreate()
    orders_data = [
        (1, 100.0),
        (1, 50.0),
        (2, 200.0),
        (2, 75.0),
        (3, 300.0),
    ]
    customers_data = [
        (1, "Alice", "Premium"),
        (2, "Bob", "Standard"),
        (3, "Charlie", "Premium"),
    ]
    orders = spark.createDataFrame(orders_data, ["customer_id", "amount"])
    customers = spark.createDataFrame(customers_data, ["customer_id", "name", "tier"])
    result = broadcast_join(orders, customers)
    result.show()
    spark.stop()
