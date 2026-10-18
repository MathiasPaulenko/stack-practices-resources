# Delta Lake: ACID writes, time travel and schema evolution.
# Companion to stackpractices.com/guides/data-lake-guide/
#
# Requires: pip install pyspark delta-spark

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession

builder = (
    SparkSession.builder.appName("DeltaLakeExample")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)
spark = configure_spark_with_delta_pip(builder).getOrCreate()

TABLE = "./lake/silver/orders"

# Write with ACID guarantees
df = spark.createDataFrame(
    [(1, "alice", 49.99), (2, "bob", 120.0)],
    ["order_id", "customer", "total"],
)
df.write.format("delta").mode("overwrite").save(TABLE)

# Time travel — read version 0 of the table
v0 = spark.read.format("delta").option("versionAsOf", 0).load(TABLE)
v0.show()

# Schema evolution — append a frame with an extra column
df_v2 = spark.createDataFrame(
    [(3, "carol", 15.0, "ES")],
    ["order_id", "customer", "total", "country"],
)
df_v2.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save(TABLE)

spark.read.format("delta").load(TABLE).show()
