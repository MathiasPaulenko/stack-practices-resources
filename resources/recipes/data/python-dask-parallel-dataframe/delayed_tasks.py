"""delayed_tasks.py — Custom task graphs with dask.delayed.

Run: python delayed_tasks.py
Requires: pip install dask pandas
"""
import pandas as pd
import dask


@dask.delayed
def load_data(n: int) -> pd.DataFrame:
    """Simulate loading a chunk of data."""
    return pd.DataFrame({
        "id": range(n, n + 100),
        "value": [float(x) * 0.1 for x in range(n, n + 100)],
    })


@dask.delayed
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean a DataFrame: filter positive values."""
    return df[df["value"] > 0].copy()


@dask.delayed
def combine(dfs: list) -> pd.DataFrame:
    """Combine multiple DataFrames and aggregate."""
    combined = pd.concat(dfs, ignore_index=True)
    return combined.groupby("id")["value"].sum().reset_index()


def build_pipeline(chunks: list[int]) -> dask.delayed:
    """Build a delayed pipeline from a list of chunk start indices."""
    loaded = [load_data(n) for n in chunks]
    cleaned = [clean(df) for df in loaded]
    return combine(cleaned)


if __name__ == "__main__":
    chunks = [0, 100, 200, 300]
    pipeline = build_pipeline(chunks)
    result = pipeline.compute()
    print(f"Combined result shape: {result.shape}")
    print(f"Total unique IDs: {result['id'].nunique()}")
    print(result.head())
