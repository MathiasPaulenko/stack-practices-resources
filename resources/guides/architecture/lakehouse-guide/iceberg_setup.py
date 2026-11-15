"""Apache Iceberg table setup with hidden partitioning and partition evolution.

Run:
    pip install pyiceberg[sql-sqlite,glue]  # or your catalog backend
    python iceberg_setup.py

Demonstrates the two features that distinguish Iceberg:
- hidden partitioning (day transform on the timestamp column)
- partition evolution (switching to hour without rewriting data)
"""
from pyiceberg.catalog import load_catalog
from pyiceberg.partitioning import PartitionField, PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.transforms import DayTransform, HourTransform
from pyiceberg.types import NestedField, StringType, TimestampType

catalog = load_catalog(
    "rest",
    **{
        "uri": "https://catalog.example.com",
        "warehouse": "s3://lakehouse/",
    },
)

table = catalog.create_table(
    identifier="silver.events",
    schema=Schema(
        NestedField(1, "event_id", StringType(), required=True),
        NestedField(2, "event_type", StringType()),
        NestedField(3, "timestamp", TimestampType()),
        NestedField(4, "payload", StringType()),
    ),
    partition_spec=PartitionSpec(
        PartitionField(source_id=3, field_id=1000, transform=DayTransform(), name="day")
    ),
)

# Partition evolution: add hour granularity without rewriting existing files.
# Old data keeps its day layout; new data lands partitioned by hour.
with table.update_spec() as update:
    update.add_field("hour", HourTransform(source_column_id=3), "hour")

print(table.spec())
