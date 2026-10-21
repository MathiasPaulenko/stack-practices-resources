# Import Data from CSV/Excel — Companion Resources

Runnable scripts for the [Import Data from CSV/Excel](https://stackpractices.com/recipes/import-csv-excel/) recipe on StackPractices.

## Contents

| File | Description |
|------|-------------|
| `import_csv.py` | Streaming CSV import: encoding detection, delimiter sniffing, Pydantic per-row validation, batch inserts into SQLite with a transaction. |
| `import_csv.js` | Node.js equivalent using `csv-parser` with error collection per row. |
| `sample-users.csv` | Sample file with edge cases: accented names, a missing name, an invalid age, and a duplicate row. |

## Usage

```bash
# Python — produces a users.db SQLite database plus a JSON report
python import_csv.py sample-users.csv users.db

# Node — prints the valid/error report
node import_csv.js sample-users.csv
```

The sample file exercises the failure modes covered in the recipe: row 4 fails validation (missing name), row 5 fails (non-numeric age), row 7 is a duplicate handled by `INSERT OR IGNORE`.

## Source

- Recipe: https://stackpractices.com/recipes/import-csv-excel/
- Recipe (ES): https://stackpractices.com/es/recipes/import-csv-excel/
