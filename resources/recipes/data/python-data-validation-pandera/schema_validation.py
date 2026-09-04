"""Pandera schema validation examples for pandas and Polars DataFrames.

Covers:
- Basic DataFrameSchema validation
- Class-based DataFrameModel with strict and coerce
- Custom checks (email validation, statistical checks)
- Schema inheritance
- Polars support
"""
import re

import pandas as pd
import pandera as pa
from pandera import Column, Check, DataFrameSchema, Field
from pandera.typing import Series


# --- Basic schema ---
basic_schema = DataFrameSchema({
    "order_id": Column(int, checks=Check.gt(0)),
    "customer_id": Column(int, nullable=False),
    "order_date": Column(pa.DateTime),
    "amount": Column(float, checks=[Check.ge(0), Check.le(100000)]),
    "status": Column(str, checks=Check.isin(["pending", "completed", "cancelled"])),
})


# --- Class-based schema ---
class OrderSchema(pa.DataFrameModel):
    order_id: Series[int] = Field(gt=0, description="Unique order identifier")
    customer_id: Series[int] = Field(nullable=False)
    order_date: Series[pa.DateTime] = Field(le="2025-12-31")
    amount: Series[float] = Field(ge=0, le=100000)
    status: Series[str] = Field(isin=["pending", "completed", "cancelled"])
    quantity: Series[int] = Field(ge=1, le=1000)

    class Config:
        strict = True
        coerce = True


# --- Custom check: email validation ---
def is_valid_email(series: pd.Series) -> pd.Series:
    """Check that all values match an email pattern."""
    pattern = r'^[\w.-]+@[\w.-]+\.\w+$'
    return series.str.match(pattern)


email_schema = DataFrameSchema({
    "email": Column(str, checks=Check(is_valid_email, element_wise=False)),
    "age": Column(int, checks=[
        Check.ge(18, error="Must be 18 or older"),
        Check.le(120, error="Age must be realistic"),
    ]),
    "phone": Column(str, checks=Check.str_matches(r'^\+?\d{10,15}$')),
})


# --- Schema inheritance ---
class BaseOrderSchema(pa.DataFrameModel):
    order_id: Series[int] = Field(gt=0)
    customer_id: Series[int] = Field(nullable=False)
    amount: Series[float] = Field(ge=0)


class ExtendedOrderSchema(BaseOrderSchema):
    status: Series[str] = Field(isin=["pending", "completed", "cancelled"])
    shipping_address: Series[str] = Field(nullable=True)

    class Config:
        strict = True
        coerce = True


if __name__ == "__main__":
    df = pd.DataFrame({
        "order_id": [1, 2, 3],
        "customer_id": [101, 102, 103],
        "order_date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"]),
        "amount": [100.0, 250.0, 75.5],
        "status": ["completed", "pending", "cancelled"],
        "quantity": [2, 1, 5],
    })
    validated = OrderSchema.validate(df)
    print("Validation passed!")
    print(validated.dtypes)
