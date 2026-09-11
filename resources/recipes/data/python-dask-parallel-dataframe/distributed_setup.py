"""distributed_setup.py — Dask Distributed scheduler setup.

Run: python distributed_setup.py
Requires: pip install dask[dataframe] distributed pandas
"""
import pandas as pd
import dask.dataframe as dd
from dask.distributed import Client


def create_client(n_workers: int = 2, threads_per_worker: int = 2,
                 memory_limit: str = "1GB") -> Client:
    """Create a local Dask distributed client."""
    return Client(n_workers=n_workers,
                  threads_per_worker=threads_per_worker,
                  memory_limit=memory_limit)


def run_groupby(client: Client, pdf: pd.DataFrame) -> pd.DataFrame:
    """Run a group-by aggregation on the distributed scheduler."""
    ddf = dd.from_pandas(pdf, npartitions=4)
    result = ddf.groupby("category")["amount"].sum().compute()
    return result


if __name__ == "__main__":
    client = create_client(n_workers=2, threads_per_worker=2, memory_limit="1GB")
    print(f"Dashboard: {client.dashboard_link}")

    pdf = pd.DataFrame({
        "category": ["a", "b", "a", "b", "a", "b"] * 100,
        "amount": [10.0, 20.0, 15.0, 25.0, 12.0, 30.0] * 100,
    })

    result = run_groupby(client, pdf)
    print(f"\nGroup-by result:\n{result}")

    client.close()
    print("\nClient closed.")
