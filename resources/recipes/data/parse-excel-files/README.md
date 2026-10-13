# Parse Excel Files in Python, JavaScript, and Java

Companion resource for [Parse Excel Files in Python, JavaScript, and Java](https://stackpractices.com/recipes/parse-excel-files/).

## Files

- `excel_parse.py` — openpyxl examples: create, read, write, and stream a large workbook.
- `excel_parse.mjs` — SheetJS (`xlsx`) examples for Node.js: create, read, write.
- `ExcelParser.java` — Apache POI example: read the first sheet of a workbook.
- `requirements.txt` — Python dependencies.
- `package.json` — Node.js dependencies.

## Usage

### Python

```bash
pip install -r requirements.txt
python excel_parse.py sample   # creates sample.xlsx (run first)
python excel_parse.py read
python excel_parse.py write
python excel_parse.py large    # streaming read with read_only=True
```

### Node.js

```bash
npm install
node excel_parse.mjs sample    # creates sample.xlsx (run first)
node excel_parse.mjs read
node excel_parse.mjs write
```

### Java

```bash
# Compile with poi-ooxml 5.3.0 on the classpath, then:
java ExcelParser sample.xlsx
```

## Notes

- `excel_parse.py large` demonstrates `read_only=True`, which streams rows instead of loading the whole workbook — the right mode for files that don't fit comfortably in RAM.
- The Java example needs `org.apache.poi:poi-ooxml` on the classpath; see the Maven snippet in the recipe.
