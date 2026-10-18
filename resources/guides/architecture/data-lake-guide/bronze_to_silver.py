# Spark job: Bronze -> Silver cleaning for the e-commerce scenario.
# Companion to stackpractices.com/guides/data-lake-guide/
#
# Requires a Spark 3.x cluster (EMR, Databricks, or local pyspark + delta-spark):
#   spark-submit --master yarn --num-executors 20 --executor-memory 8g bronze_to_silver.py

from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, to_timestamp

BRONZE_PATH = "s3://lake/bronze/events/dt=2026-10-18/"
SILVER_PATH = "s3://lake/silver/events/"

spark = SparkSession.builder.appName("bronze_to_silver").getOrCreate()

# Clean: drop null users, type timestamps, dedupe on natural key
raw = spark.read.json(BRONZE_PATH)
cleaned = (
    raw.filter("user_id is not null")
       .withColumn("event_time", to_timestamp("timestamp"))
       .withColumn("event_date", to_date("event_time"))
       .dropDuplicates(["event_id"])
)

cleaned.write.format("delta") \
    .mode("append") \
    .partitionBy("event_date") \
    .save(SILVER_PATH)

# Maintenance: compact small files, then vacuum old versions
table = DeltaTable.forPath(spark, SILVER_PATH)
table.optimize().executeCompaction()
table.vacuum(retentionHours=168)
