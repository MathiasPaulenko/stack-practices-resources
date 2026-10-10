"""Flatten nested JSON to CSV with pandas.json_normalize."""
import json
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data"

records = json.loads((DATA / "sample_nested.json").read_text(encoding="utf-8"))

df = pd.json_normalize(records, sep=".")
df.to_csv("output_pandas.csv", index=False, encoding="utf-8")

print(f"Wrote {len(df)} rows to output_pandas.csv")
print(f"Columns: {list(df.columns)}")
# Note: the `orders` array stays serialized in the cell. To unwind it
# into one row per order, use record_path="orders" with meta=["user.name"].
