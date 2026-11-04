import pandera as pa
import pandas as pd

orders_schema = pa.DataFrameSchema({
    "order_id": pa.Column(int, checks=pa.Check.unique(), nullable=False),
    "customer_id": pa.Column(int, nullable=False),
    "created_at": pa.Column(pa.DateTime, nullable=False),
    "status": pa.Column(str, checks=pa.Check.isin(["pending", "processing", "shipped", "completed", "cancelled"]), nullable=False),
    "subtotal": pa.Column(float, checks=pa.Check.ge(0), nullable=False),
    "email": pa.Column(str, checks=pa.Check.str_matches(r"^[^@]+@[^@]+\.[^@]+$"), nullable=True),
}, strict=True, coerce=True)

if __name__ == "__main__":
    df = pd.read_csv("data/orders.csv")
    try:
        validated = orders_schema.validate(df, lazy=True)
        print(f"Validation passed: {len(validated)} rows")
    except pa.errors.SchemaErrors as e:
        print(f"Validation failed: {len(e.failure_cases)} issues")
