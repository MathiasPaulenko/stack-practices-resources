"""Interop between pandas, Polars and PyArrow.

Requires: polars>=1.0, pandas>=2.0, pyarrow  (pip install polars pandas pyarrow)
"""

import pandas as pd
import polars as pl
import pyarrow as pa


def pandas_to_polars(pdf: pd.DataFrame) -> pl.DataFrame:
    """Convert a pandas DataFrame to Polars (zero-copy when possible)."""
    return pl.from_pandas(pdf)


def polars_to_pandas(plf: pl.DataFrame) -> pd.DataFrame:
    """Convert back to pandas.

    `use_pyarrow_extension_array=True` keeps Arrow-backed dtypes in pandas 2.x
    and avoids copying data.
    """
    return plf.to_pandas(use_pyarrow_extension_array=True)


def heavy_in_polars_light_in_pandas(pdf: pd.DataFrame) -> pd.DataFrame:
    """Run the heavy aggregation in Polars, return pandas for downstream use."""
    return (
        pl.from_pandas(pdf)
        .lazy()
        .filter(pl.col("amount") > 100)
        .group_by("customer")
        .agg(pl.col("amount").sum())
        .collect()
        .to_pandas()
    )


def polars_from_arrow(table: pa.Table) -> pl.DataFrame:
    """Convert a PyArrow Table to Polars."""
    return pl.from_arrow(table)


def polars_to_arrow(plf: pl.DataFrame) -> pa.Table:
    """Convert Polars to a PyArrow Table (zero-copy)."""
    return plf.to_arrow()


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")  # box-drawing chars in Polars output
    pdf = pd.DataFrame({
        "customer": ["Alice", "Bob", "Alice"],
        "amount": [100.0, 250.0, 75.0],
    })
    plf = pandas_to_polars(pdf)
    print(plf)
    print(heavy_in_polars_light_in_pandas(pdf))
    table = polars_to_arrow(plf)
    print(polars_from_arrow(table))
