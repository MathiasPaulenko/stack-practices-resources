# incremental_etl.py — incremental extraction using a high-water mark.
# Runnable companion for https://stackpractices.com/patterns/etl-extract-transform-load-pattern/
import json
import pandas as pd
from sqlalchemy import text
from pathlib import Path


class IncrementalETL:
    def __init__(self, watermark_file="watermarks.json"):
        self.watermark_file = Path(watermark_file)
        self.watermarks = self._load_watermarks()

    def _load_watermarks(self):
        if self.watermark_file.exists():
            return json.loads(self.watermark_file.read_text())
        return {}

    def _save_watermarks(self):
        self.watermark_file.write_text(
            json.dumps(self.watermarks, indent=2, default=str)
        )

    def get_watermark(self, table):
        return self.watermarks.get(table)

    def update_watermark(self, table, value):
        self.watermarks[table] = value
        self._save_watermarks()

    def extract_incremental(self, conn, table, timestamp_col="updated_at"):
        last_run = self.get_watermark(table)

        if last_run:
            query = text(
                f"SELECT * FROM {table} "
                f"WHERE {timestamp_col} > :wm ORDER BY {timestamp_col}"
            )
            df = pd.read_sql(query, conn, params={"wm": last_run})
        else:
            df = pd.read_sql(text(f"SELECT * FROM {table}"), conn)

        # Watermark from the pulled batch's max, never from now() — otherwise
        # rows updated mid-extract get skipped forever.
        if not df.empty:
            new_watermark = df[timestamp_col].max()
            self.update_watermark(table, str(new_watermark))

        return df
