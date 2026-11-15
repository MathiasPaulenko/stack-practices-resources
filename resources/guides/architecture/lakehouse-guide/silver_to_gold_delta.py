"""Silver -> Gold job: daily business aggregates as a Delta table.

Run:
    spark-submit --master yarn --num-executors 20 \
        --executor-memory 8g \
        --packages io.delta:delta-spark_2.12:3.2.0 \
        silver_to_gold_delta.py [silver_path] [gold_path]

Gold tables are a contract: dashboards and models read them directly.
Schema changes here deserve the same care as a public API change.
"""
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import count, countDistinct, sum as _sum

SILVER_PATH = sys.argv[1] if len(sys.argv) > 1 else "s3://lakehouse/silver/events/"
GOLD_PATH = sys.argv[2] if len(sys.argv) > 2 else "s3://lakehouse/gold/daily_metrics/"

spark = (
    SparkSession.builder.appName("SilverToGold")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

silver = spark.read.format("delta").load(SILVER_PATH)

daily = silver.groupBy("event_date", "event_type").agg(
    count("*").alias("total_events"),
    countDistinct("user_id").alias("unique_users"),
    _sum("amount").alias("revenue"),
)

(
    daily.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(GOLD_PATH)
)
