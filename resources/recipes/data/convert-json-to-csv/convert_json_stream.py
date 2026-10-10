"""Stream a large JSON array to CSV without loading it into memory."""
import csv
from pathlib import Path

import ijson

DATA = Path(__file__).parent / "data"

with open(DATA / "sample.json", "rb") as src, open(
    "output_stream.csv", "w", newline="", encoding="utf-8"
) as out:
    writer = None
    # "item" yields each object inside a top-level JSON array
    for record in ijson.items(src, "item"):
        if writer is None:
            writer = csv.DictWriter(out, fieldnames=record.keys())
            writer.writeheader()
        writer.writerow(record)

print("Wrote output_stream.csv")
