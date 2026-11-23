# Parameterized Test Pattern — Companion Files

Companion files for [Parameterized Test Pattern](https://stackpractices.com/patterns/parameterized-test-pattern/) on StackPractices.

## Contents

- `calculator.py` — `add`, `evaluate`, `format_currency`: the functions under test.
- `validators.py` — `validate_email`: the multi-parameter example.
- `test_parameterized.py` — all the parameterized variants from the article: `parametrize` with readable `ids`, the multi-parameter email validator, fixture-free examples, cross-product (`currency × amount`), and a CSV-driven test. Run it: `pytest test_parameterized.py -v`.
- `email_cases.csv` — the external-data variant's case table.

## What to look at

- `ids=[...]` turns `test_to_upper[4]` into `test_to_upper[camelcase]` — the failure report names the case, not its row number.
- Fetching `page_size + 1`-style probing isn't needed here, but the `pytest.raises` table shows the same pattern for error paths: one test, a table of invalid inputs.
- `_load_csv_cases` keeps the data next to the test but in a file a non-developer can edit — the external-source variant.
- `test_format_currency` is the cross-product trap: 2 decorators, 16 tests. Add a third dimension and it grows fast.
