# Parse PDF Files in Python, JavaScript and Java

Companion resource for [Parse PDF Files in Python, JavaScript and Java](https://stackpractices.com/recipes/parse-pdf-files/).

## Files

- `pdf_examples.py` — Python examples (pypdf, pdfplumber, pikepdf) runnable as standalone commands.
- `pdf_examples.mjs` — Node.js examples (pdf-parse, pdf-lib).
- `requirements.txt` — Python dependencies.
- `package.json` — Node.js dependencies.

## Usage

```bash
pip install -r requirements.txt
python pdf_examples.py sample      # creates sample.pdf first
python pdf_examples.py text
python pdf_examples.py metadata
python pdf_examples.py tables
python pdf_examples.py encrypted

npm install
node pdf_examples.mjs text         # requires sample.pdf from the step above
node pdf_examples.mjs metadata
```

## Examples

| Command | Description |
|---------|-------------|
| `sample` | Create `sample.pdf` with text and a table (run first) |
| `text` | Extract text page by page with `pypdf` |
| `metadata` | Read document info and write an updated `Producer` field |
| `tables` | Extract the table on page 2 and word coordinates with `pdfplumber` |
| `encrypted` | Encrypt a copy with `pikepdf`, then decrypt and parse it |
| `text` (mjs) | Extract text with `pdf-parse` in Node.js |
| `metadata` (mjs) | Read title/author with `pdf-lib` in Node.js |
