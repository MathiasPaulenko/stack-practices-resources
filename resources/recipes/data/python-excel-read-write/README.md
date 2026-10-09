# Read and Write Excel Files in Python (openpyxl + pandas)

Companion resource for [Read and Write Excel Files in Python](https://stackpractices.com/recipes/python-excel-read-write/).

## Files

- `excel_examples.py` — all code examples from the recipe, runnable as standalone commands.
- `requirements.txt` — Python dependencies.

## Usage

```bash
pip install -r requirements.txt
python excel_examples.py sample        # creates sample.xlsx first
python excel_examples.py pandas_read
python excel_examples.py pandas_write
python excel_examples.py openpyxl_format
python excel_examples.py openpyxl_read
python excel_examples.py formulas
python excel_examples.py append
python excel_examples.py large_file
```

## Examples

| Command | Description |
|---------|-------------|
| `sample` | Create `sample.xlsx` with demo data (run first) |
| `pandas_read` | Read one sheet and all sheets with `pd.read_excel` |
| `pandas_write` | Write a single sheet and multiple sheets |
| `openpyxl_format` | Styled report: fills, fonts, borders, freeze panes, autofilter |
| `openpyxl_read` | Read cells and ranges with `load_workbook` |
| `formulas` | Write `=SUM`/`=AVERAGE` formula cells |
| `append` | Add a sheet to an existing workbook with `mode="a"` |
| `large_file` | Streaming read with `read_only=True` |
