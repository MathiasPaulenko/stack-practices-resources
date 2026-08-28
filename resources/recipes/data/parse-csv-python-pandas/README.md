# Parse CSV Files with Python and Pandas

Companion resource for [Parse CSV Files with Python and Pandas](https://stackpractices.com/recipes/parse-csv-python-pandas/).

## Files

- `parse_csv_examples.py` — all code examples from the recipe, runnable as standalone functions.
- `sample.csv` — sample sales dataset with 10 rows for testing.
- `requirements.txt` — Python dependencies.

## Usage

```bash
pip install -r requirements.txt
python parse_csv_examples.py basic
python parse_csv_examples.py pandas_read
python parse_csv_examples.py filter
python parse_csv_examples.py chunked
python parse_csv_examples.py encoding
python parse_csv_examples.py typed
python parse_csv_examples.py memory
```

## Examples

| Command | Description |
|---------|-------------|
| `basic` | CSV parsing with the stdlib `csv` module |
| `pandas_read` | Reading CSV with `pd.read_csv` |
| `filter` | Filtering, grouping, and exporting |
| `chunked` | Chunked processing for large files |
| `encoding` | Handling encoding issues (UTF-8, latin-1, cp1252) |
| `typed` | Explicit dtype specification |
| `memory` | Memory optimization with dtype and usecols |
