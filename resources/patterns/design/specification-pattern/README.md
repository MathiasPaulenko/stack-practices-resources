# Specification Pattern — Companion

Composable invoice specifications with operator overloading (`&`, `|`, `~`)
and a repository that accepts any spec. Includes pytest coverage for leaf
specs and every composition operator.

## Run

```bash
pip install -r requirements.txt
python specifications.py   # prints critical invoices
pytest                     # runs the spec-composition tests
```

## What to look at

- `specifications.py` — `Specification` ABC, `_And`/`_Or`/`_Not` composites, concrete specs, `InvoiceRepository`
- `tests/test_specifications.py` — boundary tests plus one test per operator

Source pattern: <https://stackpractices.com/patterns/specification-pattern/>
