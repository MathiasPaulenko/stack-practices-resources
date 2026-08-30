#!/usr/bin/env python3
"""Convert a CSV file to JSON using only the Python standard library."""
import csv
import json
from pathlib import Path

CSV_PATH = Path(__file__).parent / "data" / "sample.csv"
JSON_PATH = Path(__file__).parent / "data" / "sample-std.json"


def type_cast(value: str, key: str):
    """Cast common string values to their JSON-friendly types."""
    lower = value.lower()
    if lower in ("true", "false"):
        return lower == "true"
    if key == "age":
        return int(value)
    if key == "joined":
        return value  # keep as ISO 8601 string
    return value


def main():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [{k: type_cast(v, k) for k, v in row.items()} for row in reader]

    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)

    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
