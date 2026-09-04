"""Pytest tests for Pandera schema validation.

Run with: python -m pytest test_validation.py -v
"""
import pandas as pd
import pytest
import pandera as pa
from pandera import Column, Check, DataFrameSchema

from schema_validation import OrderSchema, basic_schema
from pipeline_validation import process_orders


def test_valid_basic_schema():
    """Valid DataFrame passes basic schema validation."""
    df = pd.DataFrame({
        "order_id": [1, 2, 3],
        "customer_id": [101, 102, 103],
        "order_date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"]),
        "amount": [100.0, 250.0, 75.5],
        "status": ["completed", "pending", "cancelled"],
    })
    basic_schema.validate(df)


def test_invalid_amount_raises():
    """Negative amount raises SchemaError."""
    df = pd.DataFrame({
        "order_id": [1, 2],
        "customer_id": [101, 102],
        "order_date": pd.to_datetime(["2025-01-01", "2025-01-02"]),
        "amount": [100.0, -50.0],
        "status": ["completed", "pending"],
    })
    with pytest.raises(pa.SchemaError):
        basic_schema.validate(df)


def test_class_based_schema_valid():
    """Valid DataFrame passes class-based schema validation."""
    df = pd.DataFrame({
        "order_id": [1, 2],
        "customer_id": [101, 102],
        "order_date": pd.to_datetime(["2025-01-01", "2025-01-02"]),
        "amount": [100.0, 250.0],
        "status": ["completed", "pending"],
        "quantity": [2, 1],
    })
    OrderSchema.validate(df)


def test_pipeline_input_output():
    """Pipeline validates input and output correctly."""
    df = pd.DataFrame({
        "order_id": [1, 2],
        "amount": [100.0, 250.0],
    })
    result = process_orders(df)
    assert "amount_with_tax" in result.columns
    assert (result["amount_with_tax"] >= 0).all()


def test_strict_mode_rejects_extra_columns():
    """Strict schema rejects unexpected columns."""
    schema = DataFrameSchema(
        {"id": Column(int, checks=Check.gt(0))},
        strict=True,
    )
    df = pd.DataFrame({"id": [1], "extra": ["bad"]})
    with pytest.raises(pa.SchemaError):
        schema.validate(df)


def test_coerce_converts_strings():
    """Coerce mode converts string columns to expected types."""
    schema = DataFrameSchema({
        "id": Column(int, coerce=True),
        "amount": Column(float, coerce=True),
    })
    df = pd.DataFrame({"id": ["1", "2"], "amount": ["10.0", "20.0"]})
    result = schema.validate(df)
    assert result["id"].dtype == "int64"
    assert result["amount"].dtype == "float64"
