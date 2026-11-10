# demo.py — end-to-end ETL demo on SQLite.
# Seeds a fake source table, runs the pipeline twice (idempotency),
# then runs an incremental extraction with a watermark.
# Usage: python demo.py
import pandas as pd
from sqlalchemy import create_engine, text

from etl_pipeline import ETLPipeline
from incremental_etl import IncrementalETL

SOURCE_ROWS = [
    (1, "  Alice@Example.COM ", "Alice", "Smith", "active", "2026-01-01", "2026-07-01"),
    (2, "bob@example.com", "Bob", "Jones", "inactive", "2026-01-02", "2026-07-02"),
    (3, "carol@example.com", "Carol", "Diaz", "active", "2026-01-03", "2026-07-03"),
    (2, "bob@example.com", "Bob", "Jones", "inactive", "2026-01-02", "2026-07-02"),  # dup
]

COLS = ["id", "email", "first_name", "last_name", "status", "created_at", "updated_at"]


def seed_source(engine):
    df = pd.DataFrame(SOURCE_ROWS, columns=COLS)
    df.to_sql("customers", engine, index=False, if_exists="replace")


def main():
    source = create_engine("sqlite:///demo_source.db")
    staging = create_engine("sqlite:///demo_staging.db")
    warehouse = create_engine("sqlite:///demo_warehouse.db")

    seed_source(source)

    # The target table must exist for the delete+insert upsert
    with warehouse.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS customers"))
    pd.DataFrame(columns=COLS + ["is_active", "full_name"]).to_sql(
        "customers", warehouse, index=False
    )

    pipeline = ETLPipeline(source, staging, warehouse)

    print("\n=== Run 1 ===")
    result1 = pipeline.run("customers", "customers")

    print("\n=== Run 2 (re-run must be idempotent) ===")
    result2 = pipeline.run("customers", "customers")

    final = pd.read_sql("SELECT id, email, full_name, is_active FROM customers ORDER BY id", warehouse)
    print("\nWarehouse contents:")
    print(final.to_string(index=False))
    assert len(final) == 3, "idempotency failed: duplicate rows after re-run"
    print(f"\nRuns {result1['run_id']} / {result2['run_id']} — 3 rows, no duplicates.")

    print("\n=== Incremental extraction with watermark ===")
    inc = IncrementalETL("demo_watermarks.json")
    first = inc.extract_incremental(source, "customers")
    print(f"First run: {len(first)} rows, watermark -> {inc.get_watermark('customers')}")
    second = inc.extract_incremental(source, "customers")
    print(f"Second run: {len(second)} rows (nothing changed since watermark)")


if __name__ == "__main__":
    main()
