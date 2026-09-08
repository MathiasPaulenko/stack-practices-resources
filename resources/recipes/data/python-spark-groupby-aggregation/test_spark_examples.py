"""Tests for PySpark group-by aggregation examples.

These tests validate the structure and logic of the example functions
without requiring a real Spark cluster. They use Spark's local mode.
"""
import pytest


@pytest.fixture(scope="module")
def spark():
    from pyspark.sql import SparkSession
    session = (
        SparkSession.builder
        .appName("tests")
        .master("local[2]")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield session
    session.stop()


@pytest.fixture
def orders(spark):
    from pyspark.sql import functions as F
    data = [
        (1, "2025-01-15", 100.0, "completed", "electronics"),
        (1, "2025-01-20", 50.0, "completed", "books"),
        (2, "2025-01-15", 200.0, "cancelled", "electronics"),
        (2, "2025-02-01", 75.0, "completed", "books"),
        (3, "2025-01-10", 300.0, "completed", "electronics"),
    ]
    return spark.createDataFrame(
        data, ["customer_id", "order_date", "amount", "status", "category"]
    )


@pytest.fixture
def customers(spark):
    data = [
        (1, "Alice"),
        (2, "Bob"),
        (3, "Charlie"),
    ]
    return spark.createDataFrame(data, ["customer_id", "name"])


def test_basic_groupby(spark, orders):
    from basic_aggregation import basic_groupby
    result = basic_groupby(spark, orders)
    rows = result.collect()
    assert len(rows) == 3
    customer1 = [r for r in rows if r["customer_id"] == 1][0]
    assert customer1["total_spent"] == 150.0
    assert customer1["order_count"] == 2


def test_groupby_multiple_columns(spark, orders):
    from basic_aggregation import groupby_multiple_columns
    result = groupby_multiple_columns(spark, orders)
    rows = result.collect()
    assert len(rows) == 4
    assert "monthly_spent" in rows[0].asDict()


def test_row_number_example(orders):
    from window_functions import row_number_example
    result = row_number_example(orders)
    rows = result.collect()
    assert "order_rank" in rows[0].asDict()
    ranks = [r["order_rank"] for r in rows if r["customer_id"] == 1]
    assert ranks == [1, 2]


def test_running_total_example(orders):
    from window_functions import running_total_example
    result = running_total_example(orders)
    rows = result.filter("customer_id = 1").orderBy("order_date").collect()
    assert rows[0]["running_total"] == 100.0
    assert rows[1]["running_total"] == 150.0


def test_lag_example(orders):
    from window_functions import lag_example
    from pyspark.sql import functions as F
    result = lag_example(orders)
    rows = result.filter("customer_id = 1").orderBy(F.desc("order_date")).collect()
    assert rows[0]["prev_amount"] is not None


def test_broadcast_join(orders, customers):
    from broadcast_join import broadcast_join
    result = broadcast_join(orders, customers)
    rows = result.collect()
    assert len(rows) == 5
    assert "name" in rows[0].asDict()


def test_salt_skewed_groupby(spark):
    from skew_handling import salt_skewed_groupby
    data = [(1, 100.0)] * 100 + [(2, 50.0)] * 10
    orders = spark.createDataFrame(data, ["customer_id", "amount"])
    result = salt_skewed_groupby(orders, num_salts=5)
    rows = result.collect()
    assert len(rows) == 2
    customer1 = [r for r in rows if r["customer_id"] == 1][0]
    assert customer1["total_sum"] == 10000.0


def test_partition_tuning(spark, orders):
    from partition_tuning import repartition_before_groupby, coalesce_after_aggregation
    result = repartition_before_groupby(orders, 4)
    result = coalesce_after_aggregation(result, 2)
    rows = result.collect()
    assert len(rows) == 3
