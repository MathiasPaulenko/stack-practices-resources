"""Convert a flat JSON array to CSV with the Python standard library."""
import csv
import json
from pathlib import Path

DATA = Path(__file__).parent / "data"

records = json.loads((DATA / "sample.json").read_text(encoding="utf-8"))

# Defensive header derivation: union of keys across all records,
# not just the first one. Missing keys become empty cells.
fieldnames = sorted({key for record in records for key in record})

with open("output_std.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, restval="", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(records)

print(f"Wrote {len(records)} rows to output_std.csv")
