"""Complete ETL pipeline: extract CSV/JSON, transform with validation, load to partitioned Parquet.

Companion code for https://stackpractices.com/recipes/python-pandas-etl-pipeline/
Run: python etl_pipeline.py  (generates sample data first if missing)
"""

import logging
import time
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

EXPECTED_SCHEMA = {
    "order_id": "int64",
    "customer_id": "object",
    "order_date": "datetime64[ns]",
    "amount": "float64",
    "quantity": "Int64",
    "status": "category",
}


def extract_csv(path: str) -> pd.DataFrame:
    """Extract data from a CSV file."""
    logger.info("Extracting from %s", path)
    df = pd.read_csv(path)
    logger.info("Extracted %d rows, %d columns", len(df), len(df.columns))
    return df


def extract_json(path: str) -> pd.DataFrame:
    """Extract data from a JSON lines file."""
    logger.info("Extracting from %s", path)
    return pd.read_json(path, lines=True)


def extract_with_retry(path: str, retries: int = 3, delay: int = 5) -> pd.DataFrame:
    """Extract with retry logic for unreliable sources."""
    for attempt in range(retries):
        try:
            return pd.read_csv(path)
        except Exception as e:
            logger.warning("Attempt %d/%d failed: %s", attempt + 1, retries, e)
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
    raise RuntimeError(f"Could not read {path} after {retries} attempts")


def extract_and_merge(orders_path: str, customers_path: str) -> pd.DataFrame:
    """Extract from multiple sources and merge on a shared key."""
    orders = pd.read_csv(orders_path)
    customers = pd.read_csv(customers_path)

    orders["customer_id"] = orders["customer_id"].astype(str).str.strip()
    customers["customer_id"] = customers["customer_id"].astype(str).str.strip()

    merged = orders.merge(customers, on="customer_id", how="left")
    logger.info(
        "Merged: %d orders + %d customers = %d rows",
        len(orders), len(customers), len(merged),
    )
    return merged


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Apply transformations: type coercion, cleaning, derived columns."""
    logger.info("Starting transformation")

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").astype("Int64")

    df = df.dropna(subset=["order_date", "amount"])

    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["revenue"] = df["amount"] * df["quantity"]

    df["customer_name"] = df["customer_name"].str.strip().str.title()
    df["status"] = df["status"].astype("category")

    logger.info("Transformed to %d rows", len(df))
    return df


def transform_with_validation(df: pd.DataFrame) -> pd.DataFrame:
    """Transform with data quality checks that log and reject bad rows."""
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    negative_count = (df["amount"] < 0).sum()
    if negative_count > 0:
        logger.warning("Found %d negative amounts, filtering out", negative_count)
        df = df[df["amount"] >= 0]

    dup_count = df.duplicated(subset=["order_id"]).sum()
    if dup_count > 0:
        logger.warning("Found %d duplicate order IDs, keeping last", dup_count)
        df = df.drop_duplicates(subset=["order_id"], keep="last")

    required_cols = ["order_id", "customer_id", "order_date", "amount"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["quarter"] = df["order_date"].dt.quarter
    return df


def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Enforce the expected schema on the DataFrame."""
    for col, dtype in EXPECTED_SCHEMA.items():
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
        if str(df[col].dtype) != dtype:
            logger.info("Converting %s from %s to %s", col, df[col].dtype, dtype)
            if dtype == "datetime64[ns]":
                df[col] = pd.to_datetime(df[col], errors="coerce")
            elif dtype == "category":
                df[col] = df[col].astype("category")
            else:
                df[col] = df[col].astype(dtype)
    return df


def load_partitioned(df: pd.DataFrame, base_path: str) -> None:
    """Load to Parquet partitioned by year and month."""
    out = df.copy()
    out["year"] = out["year"].astype(str)
    out["month"] = out["month"].astype(str).str.zfill(2)

    out.to_parquet(
        base_path,
        partition_cols=["year", "month"],
        index=False,
        engine="pyarrow",
        compression="snappy",
    )
    logger.info("Partitioned output at %s/year=*/month=*", base_path)


def load_incremental(df: pd.DataFrame, path: str) -> None:
    """Append new data to an existing Parquet dataset, deduplicated."""
    if Path(path).exists():
        existing = pd.read_parquet(path)
        combined = pd.concat([existing, df], ignore_index=True)
        combined = combined.drop_duplicates(subset=["order_id"], keep="last")
    else:
        combined = df

    combined.to_parquet(path, index=False)
    logger.info("Incremental load: %d new rows, %d total", len(df), len(combined))


def read_partitioned(base_path: str, year: str, month: str | None = None) -> pd.DataFrame:
    """Read specific partitions back."""
    path = f"{base_path}/year={year}/month={month}" if month else f"{base_path}/year={year}"
    return pd.read_parquet(path)


def run_pipeline(source_path: str, destination_path: str) -> None:
    """Run the full ETL pipeline."""
    df = extract_csv(source_path)
    df = transform(df)
    load_partitioned(df, destination_path)


def run_pipeline_safe(source: str, destination: str) -> bool:
    """Run the pipeline with full error handling."""
    try:
        df = extract_with_retry(source)
        df = transform_with_validation(df)
        load_partitioned(df, destination)
        logger.info("Pipeline completed successfully")
        return True
    except Exception as e:
        logger.error("Pipeline failed: %s", e)
        return False


def make_sample_data(path: str = "data/raw/orders.csv") -> None:
    """Create a small sample orders.csv so the pipeline is runnable out of the box."""
    csv_path = Path(path)
    if csv_path.exists():
        return
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.write_text(
        "order_id,customer_id,customer_name,order_date,amount,quantity,status\n"
        "1001,C001, alice smith ,2025-01-15,120.50,2,completed\n"
        "1002,C002,bob jones,2025-01-18,89.99,1,completed\n"
        "1003,C003,carol white,2025-02-02,-15.00,1,cancelled\n"
        "1004,C001,alice smith,2025-02-10,250.00,3,completed\n"
        "1005,C004,dave brown,2025-02-14,not_a_number,1,pending\n"
        "1004,C001,alice smith,2025-02-10,250.00,3,completed\n"
        "1006,C005,erin davis,2025-03-01,42.75,5,completed\n",
        encoding="utf-8",
    )
    logger.info("Wrote sample data to %s", csv_path)


if __name__ == "__main__":
    make_sample_data()
    run_pipeline_safe("data/raw/orders.csv", "data/processed/orders")
