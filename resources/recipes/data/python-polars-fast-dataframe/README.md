# Polars: High-Performance DataFrame Operations in Python

Companion code for the [Polars fast DataFrame recipe](https://stackpractices.com/recipes/python-polars-fast-dataframe/) on StackPractices.

## Files

| File | Description |
| --- | --- |
| `polars_basics.py` | Basic DataFrame operations: select, filter, group-by, join, `when/then`, `replace_strict`, window functions, pivot |
| `lazy_pipeline.py` | Lazy evaluation: `scan_*`, query plans with `explain()`, streaming engine via `collect(engine="streaming")` |
| `pandas_interop.py` | Conversions between pandas, Polars, and PyArrow |
| `test_polars_examples.py` | Unit tests for all examples (pytest) |

## Setup

```bash
pip install "polars>=1.0" pandas pyarrow pytest
```

The examples target `polars>=1.0`. Notable 1.0 API changes used here:
`pivot(on=...)` (was `columns=`) and `collect(engine="streaming")` (was `streaming=True`).

## Running the Examples

```bash
python polars_basics.py
python lazy_pipeline.py
python pandas_interop.py
```

## Running the Tests

```bash
pytest test_polars_examples.py -v
```
