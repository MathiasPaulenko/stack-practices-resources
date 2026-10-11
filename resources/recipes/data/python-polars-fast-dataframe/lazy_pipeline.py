"""Lazy evaluation pipeline with Polars.

`pl.scan_*` builds a query plan without reading data; `.collect()` executes it
after the optimizer applies predicate pushdown and projection pushdown.

Requires: polars>=1.0  (pip install polars)
"""

import pathlib
import tempfile

import polars as pl


def build_lazy_query(lf: pl.LazyFrame) -> pl.LazyFrame:
    """Compose a lazy query: filter, derive, group by, sort.

    Nothing executes until `.collect()` is called.
    """
    return (
        lf
        .filter(pl.col("amount") > 50)
        .with_columns([
            pl.col("order_date").str.strptime(pl.Date, "%Y-%m-%d").alias("date"),
            pl.col("amount").alias("revenue"),
        ])
        .group_by("customer")
        .agg([
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("order_id").n_unique().alias("orders"),
        ])
        .sort("total_revenue", descending=True)
    )


def show_plan(lf: pl.LazyFrame) -> str:
    """Return the optimized logical plan as text.

    `explain()` shows whether the filter was pushed into the scan
    (look for FILTER vs. a predicate inside the scan node).
    """
    return lf.explain()


def collect_streaming(lf: pl.LazyFrame) -> pl.DataFrame:
    """Execute the lazy plan with the streaming engine (bounded memory).

    Polars 1.x API: `collect(engine="streaming")`.
    Pre-1.0 equivalent: `collect(streaming=True)`.
    """
    return lf.collect(engine="streaming")


def write_formats(df: pl.DataFrame, out_dir: pathlib.Path) -> dict[str, pathlib.Path]:
    """Write a DataFrame to CSV, Parquet (zstd) and IPC (Arrow)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "csv": out_dir / "output.csv",
        "parquet": out_dir / "output.parquet",
        "ipc": out_dir / "output.arrow",
    }
    df.write_csv(paths["csv"])
    df.write_parquet(paths["parquet"], compression="zstd")
    df.write_ipc(paths["ipc"])
    return paths


def _demo() -> None:
    import sys

    sys.stdout.reconfigure(encoding="utf-8")  # box-drawing chars in Polars output
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)
        df = pl.DataFrame({
            "order_id": [1, 2, 3, 4, 5],
            "customer": ["Alice", "Bob", "Alice", "Charlie", "Bob"],
            "amount": [100.0, 250.0, 75.5, 300.0, 150.0],
            "order_date": [
                "2025-01-01", "2025-01-02", "2025-01-03",
                "2025-01-04", "2025-01-05",
            ],
        })
        parquet_path = tmp_path / "orders.parquet"
        df.write_parquet(parquet_path)

        lf = pl.scan_parquet(parquet_path)
        result = build_lazy_query(lf)
        print(show_plan(result))
        print(collect_streaming(result))


if __name__ == "__main__":
    _demo()
