"""Weekly Delta Lake maintenance: compact, Z-order, vacuum, manifest.

Run:
    spark-submit --master yarn \
        --packages io.delta:delta-spark_2.12:3.2.0 \
        delta_maintenance.py [table_path] [retention_hours]

- OPTIMIZE folds small files into ~1GB targets (the #1 lakehouse fix).
- Z-ORDER colocates related data for filtered queries.
- VACUUM removes versions older than retention (irreversible).
- symlink_format_manifest lets Athena/Redshift Spectrum read the table.
"""
import sys

from delta.tables import DeltaTable
from pyspark.sql import SparkSession

TABLE_PATH = sys.argv[1] if len(sys.argv) > 1 else "s3://lakehouse/silver/events/"
RETENTION_HOURS = int(sys.argv[2]) if len(sys.argv) > 2 else 168  # 7 days

spark = (
    SparkSession.builder.appName("DeltaMaintenance")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

table = DeltaTable.forPath(spark, TABLE_PATH)

table.optimize().compact(minFileSize="10MB")
table.optimize().zOrder("user_id")
table.vacuum(retentionHours=RETENTION_HOURS)

# Manifest so engines that don't read Delta logs (e.g. Athena) can query it
table.generate("symlink_format_manifest")

print(table.history(5).select("version", "timestamp", "operation").show(truncate=False))
