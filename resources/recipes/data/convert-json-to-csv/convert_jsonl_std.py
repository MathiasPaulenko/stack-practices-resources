"""Convert a JSON Lines file (one object per line) to CSV."""
import csv
import json
from pathlib import Path

DATA = Path(__file__).parent / "data"

with open(DATA / "sample.jsonl", encoding="utf-8") as src, open(
    "output_jsonl.csv", "w", newline="", encoding="utf-8"
) as out:
    records = (json.loads(line) for line in src if line.strip())
    first = next(records)
    writer = csv.DictWriter(out, fieldnames=first.keys())
    writer.writeheader()
    writer.writerow(first)
    writer.writerows(records)

print("Wrote output_jsonl.csv")
