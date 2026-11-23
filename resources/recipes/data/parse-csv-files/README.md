# Parse CSV Files — Companion Files

Companion files for [Parse CSV Files](https://stackpractices.com/recipes/parse-csv-files/) on StackPractices.

## Contents

- `parse_csv.py` — `parse_rows`, `parse_dicts`, `parse_dicts_strict` (skip-and-log malformed rows), `sniff_delimiter` and `stream_sum` (large-file variant).
- `sample.csv` — standard CSV including a quoted field containing a comma.
- `sample_bom.csv` — UTF-8-with-BOM file, the Excel export case.
- `sample_semicolon.csv` — European-style `;`-delimited file.
- `test_parse_csv.py` — pytest suite covering all helpers. Run: `pytest test_parse_csv.py -v`.

## What to look at

- `utf-8-sig` everywhere — the one-liner that prevents the `\ufeffname` first-column bug.
- `test_quoted_field_with_comma` is the reason `split(',')` can't be trusted: the field `b@x.com, inc` must survive as one cell.
- `sniff_delimiter` + `DictReader` handles files whose delimiter you don't control.
