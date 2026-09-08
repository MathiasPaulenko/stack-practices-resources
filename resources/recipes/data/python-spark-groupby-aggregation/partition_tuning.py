"""Partition tuning examples with PySpark."""
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def tune_shuffle_partitions(spark: SparkSession, num_partitions: int):
    """Set shuffle partitions based on data size."""
    spark.conf.set("spark.sql.shuffle.partitions", str(num_partitions))


def repartition_before_groupby(orders, num_partitions=100):
    """Repartition by key before group-by to avoid skew."""
    repartitioned = orders.repartition(num_partitions, "customer_id")
    return (
        repartitioned.groupBy("customer_id")
        .agg(F.sum("amount").alias("total"))
    )


def coalesce_after_aggregation(result, num_partitions=10):
    """Coalesce after aggregation to reduce small files."""
    return result.coalesce(num_partitions)


if __name__ == "__main__":
    spark = SparkSession.builder.appName("partition-tuning").getOrCreate()
    tune_shuffle_partitions(spark, 50)
    data = [
        (1, 100.0),
        (1, 50.0),
        (2, 200.0),
        (2, 75.0),
        (3, 300.0),
    ]
    orders = spark.createDataFrame(data, ["customer_id", "amount"])
    result = repartition_before_groupby(orders, 10)
    result = coalesce_after_aggregation(result, 5)
    result.show()
    spark.stop()
