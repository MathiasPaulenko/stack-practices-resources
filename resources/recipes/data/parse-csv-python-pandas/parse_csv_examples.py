"""CSV parsing examples with Python csv module and pandas.

Run any example directly:
    python parse_csv_examples.py basic
    python parse_csv_examples.py pandas_read
    python parse_csv_examples.py filter
    python parse_csv_examples.py chunked
    python parse_csv_examples.py encoding
    python parse_csv_examples.py typed
    python parse_csv_examples.py memory
"""

import sys
import csv
import pandas as pd


def basic():
    """Basic CSV parsing with the csv module."""
    with open("sample.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row["name"], row["email"])


def pandas_read():
    """Reading CSV with pandas."""
    df = pd.read_csv("sample.csv")
    print(df.head())
    print(df.columns)
    print(df.shape)


def filter():
    """Filtering and transforming with pandas."""
    df = pd.read_csv("sample.csv")

    high_value = df[df["revenue"] > 500]
    by_region = df.groupby("region")["revenue"].sum().reset_index()
    df["margin"] = df["revenue"] - df["cost"]
    df.to_csv("sales_processed.csv", index=False)
    print(by_region)


def chunked():
    """Chunked processing for large files."""
    chunk_size = 10000
    total = 0
    for chunk in pd.read_csv("sample.csv", chunksize=chunk_size):
        total += chunk["revenue"].sum()
    print(f"Total revenue: {total}")


def encoding():
    """Handling encoding issues."""
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv("sample.csv", encoding=encoding)
            print(f"Loaded with encoding: {encoding}")
            return df
        except UnicodeDecodeError:
            continue


def typed():
    """Larger file with explicit types."""
    dtypes = {
        "id": "int32",
        "name": "string",
        "price": "float32",
        "quantity": "int16",
    }
    df = pd.read_csv(
        "sample.csv",
        dtype=dtypes,
        na_values=["", "NULL", "N/A"],
    )
    df["total"] = df["price"] * df["quantity"]
    summary = df.groupby("region")["total"].agg(["sum", "mean", "count"]).round(2)
    print(summary)


def memory():
    """Memory optimization with dtype and usecols."""
    df = pd.read_csv(
        "sample.csv",
        dtype={"id": "int32", "revenue": "float32"},
        usecols=["id", "revenue", "region"],
    )
    print(df.memory_usage(deep=True))
    df["region"] = df["region"].astype("category")
    print("After category conversion:")
    print(df.memory_usage(deep=True))


if __name__ == "__main__":
    examples = {
        "basic": basic,
        "pandas_read": pandas_read,
        "filter": filter,
        "chunked": chunked,
        "encoding": encoding,
        "typed": typed,
        "memory": memory,
    }
    if len(sys.argv) < 2 or sys.argv[1] not in examples:
        print(f"Usage: python {sys.argv[0]} <example>")
        print(f"Examples: {', '.join(examples.keys())}")
        sys.exit(1)
    examples[sys.argv[1]]()
