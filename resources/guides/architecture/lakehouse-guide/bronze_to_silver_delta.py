"""Bronze -> Silver job: clean raw events and merge them into a Delta table.

Run:
    spark-submit --master yarn --num-executors 30 \
        --executor-memory 16g \
        --packages io.delta:delta-spark_2.12:3.2.0 \
        bronze_to_silver_delta.py [bronze_path] [silver_path]

The merge is keyed on event_id, so re-running the job for the same day
updates existing rows instead of duplicating them.
"""
import sys

from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, to_timestamp

BRONZE_PATH = sys.argv[1] if len(sys.argv) > 1 else "s3://lakehouse/bronze/events/dt=2026-07-11/"
SILVER_PATH = sys.argv[2] if len(sys.argv) > 2 else "s3://lakehouse/silver/events/"

spark = (
    SparkSession.builder.appName("BronzeToSilver")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

raw = spark.read.json(BRONZE_PATH)
cleaned = (
    raw.filter("event_id is not null and user_id is not null")
    .withColumn("event_time", to_timestamp("timestamp"))
    .withColumn("event_date", to_date("event_time"))
    .dropDuplicates(["event_id"])
)

if DeltaTable.isDeltaTable(spark, SILVER_PATH):
    delta_table = DeltaTable.forPath(spark, SILVER_PATH)
    (
        delta_table.alias("target")
        .merge(cleaned.alias("source"), "target.event_id = source.event_id")
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )
else:
    (
        cleaned.write.format("delta")
        .mode("overwrite")
        .partitionBy("event_date")
        .save(SILVER_PATH)
    )
