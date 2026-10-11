"""Tests for the Polars companion examples.

Run: pytest test_polars_examples.py
Requires: polars>=1.0, pandas, pyarrow, pytest
"""

import pathlib
import tempfile

import pandas as pd
import polars as pl
import pyarrow as pa
import pytest

from lazy_pipeline import build_lazy_query, collect_streaming, write_formats
from pandas_interop import (
    heavy_in_polars_light_in_pandas,
    pandas_to_polars,
    polars_from_arrow,
    polars_to_arrow,
    polars_to_pandas,
)
from polars_basics import (
    add_derived_columns,
    group_by_customer,
    join_orders_with_customers,
    map_status_labels,
    pivot_by_month,
    sample_orders,
    select_filter_sort,
    tier_by_amount,
    window_functions,
)


@pytest.fixture()
def orders() -> pl.DataFrame:
    return sample_orders()


@pytest.fixture()
def customers() -> pl.DataFrame:
    return pl.DataFrame({
        "customer_id": [101, 102, 103],
        "name": ["Alice", "Bob", "Charlie"],
        "city": ["NYC", "LA", "Chicago"],
    })


def test_select_filter_sort(orders: pl.DataFrame) -> None:
    out = select_filter_sort(orders)
    assert out.height == 3  # amounts 250, 300, 150
    assert out["amount"].to_list() == [300.0, 250.0, 150.0]


def test_derived_columns(orders: pl.DataFrame) -> None:
    out = add_derived_columns(orders)
    assert "amount_with_tax" in out.columns
    assert out["customer_upper"].to_list()[:2] == ["ALICE", "BOB"]


def test_group_by(orders: pl.DataFrame) -> None:
    out = group_by_customer(orders).sort("customer")
    alice = out.filter(pl.col("customer") == "Alice")
    assert alice["total_spent"].item() == 175.5
    assert alice["order_count"].item() == 2
    bob = out.filter(pl.col("customer") == "Bob")
    assert bob["total_spent"].item() == 400.0


def test_join(orders: pl.DataFrame, customers: pl.DataFrame) -> None:
    orders = orders.with_columns(
        pl.col("order_id").alias("customer_id_order"),
    ).with_columns(pl.lit(101).alias("customer_id"))
    joined = join_orders_with_customers(orders, customers)
    assert joined.height == orders.height
    assert set(joined["name"].to_list()) == {"Alice"}


def test_tier(orders: pl.DataFrame) -> None:
    out = tier_by_amount(orders)
    assert out.filter(pl.col("amount") > 200)["tier"].to_list() == ["high", "high"]
    assert "low" in out["tier"].to_list()


def test_replace_strict_mapping(orders: pl.DataFrame) -> None:
    out = map_status_labels(orders)
    assert set(out["status_label"].to_list()) == {"pending"}


def test_window_functions(orders: pl.DataFrame) -> None:
    out = window_functions(orders)
    for col in ("running_total", "order_seq", "prev_amount", "ma_3"):
        assert col in out.columns


def test_pivot(orders: pl.DataFrame) -> None:
    pivoted = pivot_by_month(orders)
    # All sample orders are in January 2025 -> single month column "1"
    assert "customer" in pivoted.columns
    assert pivoted.height == 3


def test_lazy_pipeline() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "orders.parquet"
        sample_orders().write_parquet(path)
        lf = pl.scan_parquet(path)
        result = collect_streaming(build_lazy_query(lf))
        assert result.height == 3
        assert "total_revenue" in result.columns


def test_write_formats(orders: pl.DataFrame) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = write_formats(orders, pathlib.Path(tmp))
        for p in paths.values():
            assert p.exists() and p.stat().st_size > 0
        assert pl.read_parquet(paths["parquet"]).equals(orders)


def test_pandas_interop() -> None:
    pdf = pd.DataFrame({"customer": ["A", "B"], "amount": [10.0, 200.0]})
    plf = pandas_to_polars(pdf)
    assert plf.height == 2
    back = polars_to_pandas(plf)
    assert back.shape[0] == 2
    out = heavy_in_polars_light_in_pandas(pdf)
    assert out["amount"].to_list() == [200.0]


def test_arrow_interop(orders: pl.DataFrame) -> None:
    table = polars_to_arrow(orders)
    assert isinstance(table, pa.Table)
    back = polars_from_arrow(table)
    assert back.shape == orders.shape
