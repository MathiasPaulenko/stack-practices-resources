"""Runnable ETL pipeline: incremental extraction, validation, transform, upsert load.

Companion to https://stackpractices.com/guides/etl-pipeline-guide/
Uses sqlite3 so it runs anywhere; the Postgres/psycopg2 equivalents are the
same shapes with %s placeholders instead of ?.
"""

import sqlite3
from dataclasses import dataclass
from typing import Callable, List


class ValidationError(Exception):
    """Raised when one or more validators reject the batch."""
    pass


class IncrementalExtractor:
    """Pull only rows changed since the last run, tracked by watermark.

    The query orders by the watermark column (not the id) so a truncated
    batch cannot hide rows behind the new watermark.
    """

    def __init__(self, conn: sqlite3.Connection, watermark_table: str = "etl_watermarks"):
        self.conn = conn
        self.watermark_table = watermark_table
        self.conn.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.watermark_table} (
                table_name TEXT PRIMARY KEY,
                last_ts TEXT
            )"""
        )
        self.conn.commit()

    def extract_incremental(self, table: str, ts_column: str = "updated_at",
                            batch_size: int = 1000) -> List[dict]:
        row = self.conn.execute(
            f"SELECT last_ts FROM {self.watermark_table} WHERE table_name = ?",
            (table,),
        ).fetchone()
        last_ts = row[0] if row else "0000-01-01"

        cur = self.conn.execute(
            f"SELECT * FROM {table} WHERE {ts_column} > ? "
            f"ORDER BY {ts_column}, rowid LIMIT ?",
            (last_ts, batch_size),
        )
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]

        if rows:
            new_wm = str(rows[-1][ts_column])
            self.conn.execute(
                f"""INSERT INTO {self.watermark_table} (table_name, last_ts)
                    VALUES (?, ?)
                    ON CONFLICT(table_name) DO UPDATE SET last_ts = excluded.last_ts""",
                (table, new_wm),
            )
            self.conn.commit()
        return rows


@dataclass
class TransformResult:
    rows: List[dict]
    errors: List[str]


class DataTransformer:
    """Validators run first (fail fast), then transforms in order.

    A validator takes a list of dicts and returns a list of error strings;
    empty means pass.
    """

    def __init__(self):
        self.validators: List[Callable] = []
        self.transforms: List[Callable] = []

    def add_validator(self, fn: Callable):
        self.validators.append(fn)

    def add_transform(self, fn: Callable):
        self.transforms.append(fn)

    def transform(self, rows: List[dict]) -> List[dict]:
        errors = []
        for v in self.validators:
            errors.extend(v(rows) or [])
        if errors:
            raise ValidationError(f"{len(errors)} validation error(s): {errors[:5]}")
        for t in self.transforms:
            rows = t(rows)
        return rows


def validate_no_null_ids(rows: List[dict], id_column: str = "id") -> List[str]:
    return [f"row {i} has null {id_column}" for i, r in enumerate(rows) if r.get(id_column) is None]


def normalize_emails(rows: List[dict], column: str = "email") -> List[dict]:
    for r in rows:
        if r.get(column):
            r[column] = r[column].strip().lower()
    return rows


def add_order_total(rows: List[dict]) -> List[dict]:
    for r in rows:
        qty = r.get("quantity") or 0
        price = r.get("unit_price") or 0
        discount = r.get("discount") or 0
        r["order_total"] = round(qty * price * (1 - discount), 2)
    return rows


class UpsertLoader:
    """Idempotent load: re-running the same batch yields the same table."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def upsert(self, rows: List[dict], table: str, key: str = "id") -> int:
        if not rows:
            return 0
        cols = list(rows[0].keys())
        non_key = [c for c in cols if c != key]
        update = ", ".join(f"{c} = excluded.{c}" for c in non_key)
        sql = (
            f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))}) "
            f"ON CONFLICT({key}) DO UPDATE SET {update}"
        )
        self.conn.executemany(sql, [tuple(r[c] for c in cols) for r in rows])
        self.conn.commit()
        return len(rows)
