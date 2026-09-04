"""Pipeline validation with Pandera: validate at input and output boundaries.

This module shows how to validate DataFrames at each stage of a pipeline
using Pandera schemas. It includes error handling with lazy validation.
"""
import pandas as pd
import pandera as pa
from pandera import Column, Check, DataFrameSchema
from pandera import check_input, check_output


input_schema = DataFrameSchema({
    "order_id": Column(int, checks=Check.gt(0)),
    "amount": Column(float, checks=Check.ge(0)),
})

output_schema = DataFrameSchema({
    "order_id": Column(int, checks=Check.gt(0)),
    "amount": Column(float, checks=Check.ge(0)),
    "amount_with_tax": Column(float, checks=Check.ge(0)),
})


def process_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Validate input, transform, validate output."""
    df = input_schema.validate(df)
    df["amount_with_tax"] = df["amount"] * 1.1
    return output_schema.validate(df)


def validate_with_error_handling(df: pd.DataFrame, schema: DataFrameSchema) -> pd.DataFrame:
    """Validate with lazy=True to collect all errors at once."""
    try:
        return schema.validate(df, lazy=True)
    except pa.SchemaErrors as e:
        print(f"Found {len(e.failure_cases)} validation failures:")
        print(e.failure_cases[["column", "check", "failure_case", "index"]])
        raise


# Decorator-based validation
@check_input(input_schema)
@check_output(output_schema)
def enrich_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Validate input and output automatically via decorators."""
    df["amount_with_tax"] = df["amount"] * 1.1
    return df


if __name__ == "__main__":
    df = pd.DataFrame({
        "order_id": [1, 2, 3],
        "amount": [100.0, 250.0, 75.5],
    })
    result = process_orders(df)
    print("Pipeline validation passed!")
    print(result)
