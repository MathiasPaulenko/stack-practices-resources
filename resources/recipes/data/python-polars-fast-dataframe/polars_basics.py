"""Basic Polars DataFrame operations: create, select, filter, group by, join.

Requires: polars>=1.0  (pip install polars)
"""

import polars as pl


def sample_orders() -> pl.DataFrame:
    return pl.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "customer": ["Alice", "Bob", "Alice", "Charlie", "Bob"],
        "amount": [100.0, 250.0, 75.5, 300.0, 150.0],
        "order_date": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"],
    })


def select_filter_sort(df: pl.DataFrame) -> pl.DataFrame:
    """Select columns, filter rows, sort descending."""
    return (
        df.select(["order_id", "customer", "amount"])
        .filter(pl.col("amount") > 100)
        .sort("amount", descending=True)
    )


def add_derived_columns(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns([
        (pl.col("amount") * 1.1).alias("amount_with_tax"),
        pl.col("customer").str.to_uppercase().alias("customer_upper"),
    ])


def group_by_customer(df: pl.DataFrame) -> pl.DataFrame:
    return df.group_by("customer").agg([
        pl.col("amount").sum().alias("total_spent"),
        pl.col("order_id").count().alias("order_count"),
        pl.col("amount").mean().alias("avg_order"),
    ])


def join_orders_with_customers(
    orders: pl.DataFrame, customers: pl.DataFrame
) -> pl.DataFrame:
    """Inner join on customer_id."""
    return orders.join(customers, on="customer_id", how="inner")


def tier_by_amount(df: pl.DataFrame) -> pl.DataFrame:
    """Conditional tier with when/then/otherwise."""
    return df.with_columns([
        pl.when(pl.col("amount") > 200)
        .then(pl.lit("high"))
        .when(pl.col("amount") > 100)
        .then(pl.lit("medium"))
        .otherwise(pl.lit("low"))
        .alias("tier"),
    ])


def map_status_labels(df: pl.DataFrame) -> pl.DataFrame:
    """Map short status codes to labels.

    Uses replace_strict (NOT map_elements with a dict, which raises TypeError).
    `default` keeps the original value when a code has no mapping.
    """
    if "status" not in df.columns:
        df = df.with_columns(
            pl.lit("P").alias("status")
        )
    return df.with_columns([
        pl.col("status").replace_strict(
            {"P": "pending", "C": "completed", "X": "cancelled"},
            default=pl.col("status"),
        ).alias("status_label"),
    ])


def window_functions(df: pl.DataFrame) -> pl.DataFrame:
    """Per-customer running totals, ranking, lag, and moving average."""
    return df.with_columns([
        pl.col("amount").cum_sum().over("customer").alias("running_total"),
        pl.col("order_id").rank().over("customer").alias("order_seq"),
        pl.col("amount").shift(1).over("customer").alias("prev_amount"),
        pl.col("amount").rolling_mean(window_size=3).over("customer").alias("ma_3"),
    ])


def pivot_by_month(df: pl.DataFrame) -> pl.DataFrame:
    """Pivot: rows=customer, columns=month, values=amount.

    Note: the `on` parameter was called `columns` before Polars 1.0.
    """
    with_month = df.with_columns(
        pl.col("order_date").str.strptime(pl.Date, "%Y-%m-%d").dt.month().alias("month")
    )
    return with_month.pivot(
        on="month", index="customer", values="amount", aggregate_function="sum"
    )


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")  # box-drawing chars in Polars output
    df = sample_orders()
    print(select_filter_sort(df))
    print(group_by_customer(df))
    print(tier_by_amount(df))
    print(pivot_by_month(df))
