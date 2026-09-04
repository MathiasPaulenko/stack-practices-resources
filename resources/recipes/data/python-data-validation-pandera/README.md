# Pandera DataFrame Schema Validation — Companion Resource

Companion code for the StackPractices recipe [Validate DataFrame Schemas with Pandera](https://stackpractices.com/recipes/python-data-validation-pandera/).

## Contents

- `schema_validation.py` — Basic DataFrameSchema, class-based DataFrameModel, custom email checks, and schema inheritance.
- `pipeline_validation.py` — Input/output validation at pipeline boundaries, lazy error handling, and decorator-based validation.
- `test_validation.py` — Pytest tests covering valid data, invalid data, strict mode, coercion, and pipeline validation.
- `meta.json` — Resource metadata.

## Running

```bash
pip install pandera pandas pytest
python -m pytest test_validation.py -v
```

## Key concepts

- **DataFrameSchema**: dictionary-based schema for quick validation.
- **DataFrameModel**: class-based schema for reusable, inheritable schemas.
- **Custom checks**: element-wise and series-level validation functions.
- **Coercion**: automatic type conversion before validation.
- **Strict mode**: reject unexpected columns to catch schema drift.
- **Lazy validation**: collect all errors at once instead of stopping at the first.
- **Pipeline validation**: validate at input and output boundaries.
- **Pytest integration**: use schema validation as CI gates.
