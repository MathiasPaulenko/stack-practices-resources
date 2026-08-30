#!/usr/bin/env python3
"""Convert a CSV file to JSON with pandas, casting types and formatting dates."""
import pandas as pd
from pathlib import Path

CSV_PATH = Path(__file__).parent / "data" / "sample.csv"


def main():
    df = pd.read_csv(CSV_PATH)
    df["joined"] = pd.to_datetime(df["joined"])
    df["active"] = df["active"].astype(bool)
    json_data = df.to_json(orient="records", date_format="iso")
    print(json_data)


if __name__ == "__main__":
    main()
