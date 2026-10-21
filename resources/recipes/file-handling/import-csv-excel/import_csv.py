"""Streaming CSV import with per-row validation, encoding detection,
delimiter sniffing, and batch inserts into SQLite.

Usage: python import_csv.py sample-users.csv users.db
"""

import csv
import json
import sqlite3
import sys
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

BATCH_SIZE = 1000


class UserImport(BaseModel):
    name: str = Field(min_length=1)
    email: str
    age: int


def open_with_encoding(file_path: str):
    """Open a file trying UTF-8 first, then common Windows encodings."""
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            f = open(file_path, newline="", encoding=encoding)
            f.read(4096)
            f.seek(0)
            return f
        except UnicodeDecodeError:
            f.close()
    raise UnicodeDecodeError("unknown", b"", 0, 1, "could not decode file")


def detect_delimiter(file_path: str) -> str:
    """Detect the most likely delimiter in a CSV file."""
    with open(file_path, "r", encoding="utf-8") as f:
        sample = f.read(1024)
        return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter


def import_users_csv(file_path: str):
    """Stream rows, validate each one, collect errors with row numbers."""
    valid, errors = [], []
    delimiter = detect_delimiter(file_path)
    with open_with_encoding(file_path) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row_num, row in enumerate(reader, start=2):
            normalized = {k.strip().lower(): v for k, v in row.items()}
            try:
                user = UserImport(**normalized)
                valid.append(user.model_dump())
            except (ValidationError, ValueError) as e:
                errors.append({"row": row_num, "error": str(e)})
    return valid, errors


def batch_insert(db_path: str, rows: list[dict]) -> int:
    """Insert validated rows in batches inside one transaction."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(name TEXT, email TEXT UNIQUE, age INTEGER)"
        )
        conn.execute("BEGIN")
        for i in range(0, len(rows), BATCH_SIZE):
            conn.executemany(
                "INSERT OR IGNORE INTO users (name, email, age) "
                "VALUES (:name, :email, :age)",
                rows[i:i + BATCH_SIZE],
            )
        conn.commit()
        return conn.total_changes
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "sample-users.csv"
    db = sys.argv[2] if len(sys.argv) > 2 else "users.db"

    valid, errors = import_users_csv(csv_path)
    inserted = batch_insert(db, valid)

    print(json.dumps(
        {"valid": len(valid), "errors": errors, "inserted": inserted},
        indent=2,
    ))
