# test_etl_pipeline.py — pytest suite for the ETL pipeline on SQLite.
# Run: pytest test_etl_pipeline.py -v
import pandas as pd
import pytest
from sqlalchemy import create_engine, text

from etl_pipeline import ETLPipeline
from incremental_etl import IncrementalETL

COLS = ["id", "email", "first_name", "last_name", "status", "created_at", "updated_at"]

ROWS = [
    (1, "  Alice@Example.COM ", "Alice", "Smith", "active", "2026-01-01", "2026-07-01"),
    (2, "bob@example.com", "Bob", "Jones", "inactive", "2026-01-02", "2026-07-02"),
    (3, "carol@example.com", "Carol", "Diaz", "active", "2026-01-03", "2026-07-03"),
    (2, "bob@example.com", "Bob", "Jones", "inactive", "2026-01-02", "2026-07-02"),
    (4, "dave@example.com", None, None, "active", "2026-01-04", "2026-07-04"),
]


@pytest.fixture()
def engines(tmp_path):
    source = create_engine(f"sqlite:///{tmp_path}/source.db")
    staging = create_engine(f"sqlite:///{tmp_path}/staging.db")
    warehouse = create_engine(f"sqlite:///{tmp_path}/warehouse.db")

    pd.DataFrame(ROWS, columns=COLS).to_sql("customers", source, index=False)
    pd.DataFrame(columns=COLS + ["is_active", "full_name"]).to_sql(
        "customers", warehouse, index=False
    )
    return source, staging, warehouse


def test_full_run_loads_clean_rows(engines):
    source, staging, warehouse = engines
    result = ETLPipeline(source, staging, warehouse).run("customers", "customers")

    final = pd.read_sql("SELECT * FROM customers ORDER BY id", warehouse)
    assert result["rows_processed"] == 4  # 5 source rows, 1 duplicate dropped
    assert len(final) == 4
    assert final.loc[0, "email"] == "alice@example.com"  # normalized
    assert str(final.loc[0, "is_active"]) in ("1", "True")  # sqlite returns TEXT here
    assert final.loc[0, "full_name"] == "Alice Smith"


def test_extract_writes_run_id_staging_table(engines):
    source, staging, warehouse = engines
    p = ETLPipeline(source, staging, warehouse, run_id="test123")
    p.extract("customers")

    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table'", staging
    )["name"].tolist()
    assert "stg_customers_test123" in tables


def test_rerun_is_idempotent(engines):
    source, staging, warehouse = engines
    p = ETLPipeline(source, staging, warehouse)
    p.run("customers", "customers")
    p.run("customers", "customers")

    count = pd.read_sql("SELECT COUNT(*) AS n FROM customers", warehouse)["n"][0]
    assert count == 4


def test_incremental_extracts_only_new_rows(engines, tmp_path):
    source, _, _ = engines
    inc = IncrementalETL(tmp_path / "watermarks.json")

    first = inc.extract_incremental(source, "customers")
    assert len(first) == 5

    # Nothing changed: second run returns empty
    second = inc.extract_incremental(source, "customers")
    assert second.empty

    # New row arrives after the watermark
    with source.begin() as conn:
        conn.execute(text(
            "INSERT INTO customers VALUES "
            "(5, 'eve@example.com', 'Eve', 'Lee', 'active', '2026-01-05', '2026-07-10')"
        ))
    third = inc.extract_incremental(source, "customers")
    assert len(third) == 1
    assert third.iloc[0]["email"] == "eve@example.com"
    assert inc.get_watermark("customers") == "2026-07-10"


def test_watermark_persists_across_instances(engines, tmp_path):
    source, _, _ = engines
    wfile = tmp_path / "watermarks.json"
    IncrementalETL(wfile).extract_incremental(source, "customers")

    fresh = IncrementalETL(wfile)
    assert fresh.get_watermark("customers") == "2026-07-04"
