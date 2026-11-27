import csv
import json
import os
import time
from pathlib import Path
from typing import Generator, Callable

def read_csv_stream(path: str | Path, encoding: str = 'utf-8') -> Generator[dict, None, None]:
    """Yield rows from a CSV file one at a time without loading it all."""
    with open(path, 'r', encoding=encoding, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def transform_rows(rows: Generator[dict, None, None],
                   transformer: Callable[[dict], dict | None]) -> Generator[dict, None, None]:
    """Apply a transformation function to each row, skipping None results."""
    for row in rows:
        result = transformer(row)
        if result is not None:
            yield result

def write_jsonl_stream(path: str | Path, rows: Generator[dict, None, None],
                       flush_interval: int = 1000) -> int:
    """Write rows as JSONL, flushing periodically. Returns row count."""
    tmp_path = str(path) + '.tmp'
    count = 0
    with open(tmp_path, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False))
            f.write('\n')
            count += 1
            if count % flush_interval == 0:
                f.flush()
    os.replace(tmp_path, path)
    return count

def etl_pipeline(input_csv: str, output_jsonl: str,
                 transformer: Callable[[dict], dict | None]) -> None:
    """Full ETL: read CSV -> transform -> write JSONL with progress."""
    start = time.time()
    rows = read_csv_stream(input_csv)
    transformed = transform_rows(rows, transformer)

    # Wrap with progress tracking
    def with_progress(gen: Generator[dict, None, None]) -> Generator[dict, None, None]:
        count = 0
        for item in gen:
            count += 1
            if count % 10000 == 0:
                elapsed = time.time() - start
                rate = count / elapsed if elapsed > 0 else 0
                print(f"  Processed {count:,} rows ({rate:.0f} rows/s)")
            yield item

    total = write_jsonl_stream(output_jsonl, with_progress(transformed))
    elapsed = time.time() - start
    print(f"ETL complete: {total:,} rows in {elapsed:.1f}s ({total/elapsed:.0f} rows/s)")

# Usage
# def filter_active_users(row: dict) -> dict | None:
#     if row.get('status') != 'active':
#         return None
#     return {'id': row['id'], 'email': row['email'].lower(), 'name': row['name']}
# etl_pipeline('users.csv', 'users.jsonl', filter_active_users)
