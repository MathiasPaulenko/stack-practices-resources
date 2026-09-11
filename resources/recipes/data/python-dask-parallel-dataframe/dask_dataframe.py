"""dask_dataframe.py — Basic Dask DataFrame operations.

Run: python dask_dataframe.py
Requires: pip install dask[dataframe] pandas
"""
import pandas as pd
import dask.dataframe as dd


def create_sample_dataframe() -> pd.DataFrame:
    """Create a small pandas DataFrame for testing."""
    return pd.DataFrame({
        "order_id": range(1000),
        "customer_id": [f"c{i % 50}" for i in range(1000)],
        "amount": [10.0 + i * 0.5 for i in range(1000)],
        "category": ["electronics" if i % 2 == 0 else "books" for i in range(1000)],
    })


def to_dask(pdf: pd.DataFrame, npartitions: int = 4) -> dd.DataFrame:
    """Convert a pandas DataFrame to a Dask DataFrame."""
    return dd.from_pandas(pdf, npartitions=npartitions)


def lazy_groupby(ddf: dd.DataFrame) -> dd.DataFrame:
    """Build a lazy group-by aggregation (no execution yet)."""
    return (
        ddf
        .groupby("customer_id")
        .agg({"amount": "sum", "order_id": "count"})
        .reset_index()
        .sort_values("amount", ascending=False)
    )


def lazy_filter(ddf: dd.DataFrame, min_amount: float = 100.0) -> dd.DataFrame:
    """Build a lazy filter operation."""
    return ddf[ddf["amount"] > min_amount]


if __name__ == "__main__":
    pdf = create_sample_dataframe()
    ddf = to_dask(pdf, npartitions=4)
    print(f"Partitions: {ddf.npartitions}")
    print(f"Divisions: {ddf.divisions}")

    result = lazy_groupby(ddf)
    df = result.compute()
    print(f"\nTop 5 customers by amount:\n{df.head()}")

    filtered = lazy_filter(ddf, min_amount=500.0)
    print(f"\nRows with amount > 500: {len(filtered.compute())}")
