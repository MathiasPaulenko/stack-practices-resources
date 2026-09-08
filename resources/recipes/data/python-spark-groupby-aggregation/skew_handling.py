"""Data skew handling with the salting technique in PySpark."""
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import floor, rand


def salt_skewed_groupby(orders, num_salts=10):
    """Split skewed keys with salt, aggregate in two stages."""
    salted = orders.withColumn("salt", floor(rand() * num_salts).cast("int"))
    partial = (
        salted.groupBy("customer_id", "salt")
        .agg(F.sum("amount").alias("partial_sum"))
    )
    final = (
        partial.groupBy("customer_id")
        .agg(F.sum("partial_sum").alias("total_sum"))
    )
    return final


if __name__ == "__main__":
    spark = SparkSession.builder.appName("skew-handling").getOrCreate()
    # Customer 1 has many more rows (skewed)
    data = [(1, 100.0)] * 1000 + [(2, 50.0)] * 10 + [(3, 75.0)] * 5
    orders = spark.createDataFrame(data, ["customer_id", "amount"])
    result = salt_skewed_groupby(orders)
    result.show()
    spark.stop()
