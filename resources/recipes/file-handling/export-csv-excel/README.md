# Export Data to CSV and Excel Files — Companion

Companion repository for the [Export Data to CSV and Excel Files recipe](https://stackpractices.com/recipes/export-csv-excel/).

## Contents

| File | Language | Description |
| --- | --- | --- |
| `export_csv.py` | Python | CSV/Excel export with pandas, streaming, ZIP, and formulas |
| `sanitize_csv.py` | Python | CSV injection sanitization utilities with tests |
| `export_excel.js` | JavaScript | CSV/Excel export with fast-csv, xlsx, and Express streaming endpoint |
| `ExportExcel.java` | Java | CSV/Excel export with Apache Commons CSV and POI (incl. SXSSF) |
| `requirements.txt` | Python | Dependencies |
| `package.json` | Node.js | Dependencies |
| `pom.xml` | Java | Maven dependencies |

## Quick Start

### Python

```bash
pip install -r requirements.txt
python export_csv.py
python sanitize_csv.py  # run sanitization tests
```

### JavaScript

```bash
npm install
node export_excel.js
```

### Java

```bash
mvn compile
mvn exec:java -Dexec.mainClass="ExportExcel"
```

## Key Features

- **In-memory export**: pandas `to_csv`, SheetJS `XLSX.writeFile`, Apache POI `XSSFWorkbook`
- **Streaming export**: Python `csv.writer` with generator, Node.js `fast-csv` pipe, Java `SXSSFWorkbook` with sliding window
- **CSV injection sanitization**: Prefix `=`, `+`, `-`, `@` with single quote
- **Express.js endpoint**: Streaming CSV with error handling and abort signal
- **Multi-sheet Excel**: pandas `ExcelWriter` with `openpyxl` engine
- **ZIP export**: Multiple CSV files as a single ZIP archive
- **Excel formulas**: `openpyxl` formula writing with `=SUM()`
