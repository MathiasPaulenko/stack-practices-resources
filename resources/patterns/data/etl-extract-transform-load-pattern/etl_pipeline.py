# etl_pipeline.py — ETL pipeline with extract, transform, load stages.
# Runnable companion for https://stackpractices.com/patterns/etl-extract-transform-load-pattern/
# Works with any SQLAlchemy engine; tests and demo.py use SQLite.
import pandas as pd
from datetime import datetime
from sqlalchemy import text, bindparam
import logging
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ETLPipeline:
    def __init__(self, source_conn, staging_conn, warehouse_conn, run_id=None):
        self.source = source_conn
        self.staging = staging_conn
        self.warehouse = warehouse_conn
        self.run_id = run_id or hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]

    def run(self, source_table, target_table, since=None):
        logger.info(f"ETL run {self.run_id} started for {source_table} -> {target_table}")

        try:
            # Stage 1: Extract
            raw_data = self.extract(source_table, since)

            # Stage 2: Transform
            transformed_data = self.transform(raw_data)

            # Stage 3: Load
            self.load(transformed_data, target_table)

            logger.info(f"ETL run {self.run_id} completed successfully")
            return {"run_id": self.run_id, "rows_processed": len(transformed_data)}

        except Exception as e:
            logger.error(f"ETL run {self.run_id} failed: {e}")
            raise

    def extract(self, table, since=None):
        logger.info(f"Extracting from {table} since {since}")
        query = f"SELECT * FROM {table}"
        if since:
            query += " WHERE updated_at >= :since"

        df = pd.read_sql(
            text(query), self.source,
            params={"since": since} if since else None,
        )
        df["_etl_run_id"] = self.run_id
        df["_etl_extracted_at"] = datetime.now()

        # Write to a staging table namespaced by run id
        staging_table = f"stg_{table}_{self.run_id}"
        df.to_sql(staging_table, self.staging, index=False, if_exists="replace")
        logger.info(f"Extracted {len(df)} rows to {staging_table}")

        return df

    def transform(self, df):
        logger.info(f"Transforming {len(df)} rows")

        df = df.drop_duplicates(subset=["id"])

        if "email" in df.columns:
            df["email"] = df["email"].str.lower().str.strip()

        if "created_at" in df.columns:
            df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

        if "status" in df.columns:
            df["is_active"] = df["status"] == "active"
        if {"first_name", "last_name"} <= set(df.columns):
            df["full_name"] = df["first_name"] + " " + df["last_name"]

        # Drop ETL metadata columns
        df = df.drop(columns=["_etl_run_id", "_etl_extracted_at"], errors="ignore")

        df = df.dropna(subset=["id"])
        logger.info(f"Transformed to {len(df)} rows")
        return df

    def load(self, df, target_table):
        logger.info(f"Loading {len(df)} rows to {target_table}")

        # Upsert: delete the ids we're about to write, then insert.
        # The expanding IN bind is portable (SQLite, Postgres, MySQL);
        # the article shows the Postgres-specific `id = ANY(:ids)` variant.
        if not df.empty:
            stmt = text(
                f"DELETE FROM {target_table} WHERE id IN :ids"
            ).bindparams(bindparam("ids", expanding=True))
            with self.warehouse.begin() as conn:
                conn.execute(stmt, {"ids": df["id"].tolist()})

        df.to_sql(target_table, self.warehouse, index=False, if_exists="append")
        logger.info(f"Loaded {len(df)} rows to {target_table}")

    def staging_table_name(self, table):
        return f"stg_{table}_{self.run_id}"
