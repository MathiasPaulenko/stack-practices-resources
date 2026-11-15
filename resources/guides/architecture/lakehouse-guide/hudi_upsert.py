"""Apache Hudi record-level upserts + incremental read.

Run:
    spark-submit --master yarn \
        --packages org.apache.hudi:hudi-spark3.5-bundle_2.12:0.15.0 \
        hudi_upsert.py [table_path]

- recordkey.field identifies each row (enables upsert)
- precombine.field resolves same-key conflicts (latest updated_at wins)
- query.type=incremental turns the table into a changelog feed
"""
import sys

from pyspark.sql import SparkSession

TABLE_PATH = sys.argv[1] if len(sys.argv) > 1 else "s3://lakehouse/hudi/customer_orders"
BEGIN_INSTANT = sys.argv[2] if len(sys.argv) > 2 else "20240101000000"

spark = SparkSession.builder.appName("HudiUpsert").getOrCreate()

# df: incoming batch (e.g. CDC feed) with order_id + updated_at columns
df = spark.createDataFrame(
    [("ord-001", "cust-123", 99.99, "shipped", "2024-01-01T00:00:00")],
    ["order_id", "customer_id", "total", "status", "updated_at"],
)

(
    df.write.format("hudi")
    .option("hoodie.table.name", "customer_orders")
    .option("hoodie.datasource.write.recordkey.field", "order_id")
    .option("hoodie.datasource.write.precombine.field", "updated_at")
    .option("hoodie.datasource.write.operation", "upsert")
    .mode("append")
    .save(TABLE_PATH)
)

# Incremental read — only records changed since BEGIN_INSTANT
changed = (
    spark.read.format("hudi")
    .option("hoodie.datasource.query.type", "incremental")
    .option("hoodie.datasource.read.begin.instanttime", BEGIN_INSTANT)
    .load(TABLE_PATH)
)
changed.show(truncate=False)
