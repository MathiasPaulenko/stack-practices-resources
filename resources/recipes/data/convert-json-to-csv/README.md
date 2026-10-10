# Convert JSON to CSV — companion examples

This folder contains runnable examples for the StackPractices recipe
[Convert JSON to CSV](https://stackpractices.com/recipes/convert-json-to-csv/).

## Files

| File | Description |
| --- | --- |
| `data/sample.json` | Flat JSON array of objects |
| `data/sample_nested.json` | Nested JSON with objects and an array field |
| `data/sample.jsonl` | JSON Lines (one object per line) |
| `convert_json_std.py` | Python standard library version (`csv.DictWriter`) with defensive key-union headers |
| `convert_json_pandas.py` | pandas version with `json_normalize` for nested objects |
| `convert_json_stream.py` | ijson streaming version for files larger than memory |
| `convert_jsonl_std.py` | JSON Lines to CSV with the standard library |
| `requirements.txt` | Python dependencies |
| `convert_json_manual.mjs` | Dependency-free Node.js version |
| `convert_json_json2csv.mjs` | Node.js version with `@json2csv` (unwind of arrays) |
| `package.json` | Node dependencies and scripts |
| `pom.xml` | Maven project for the Java example |
| `src/main/java/JsonToCsv.java` | Java version with Jackson + Apache Commons CSV |

## Running the examples

### Python

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python convert_json_std.py
python convert_json_pandas.py
python convert_json_stream.py
python convert_jsonl_std.py
```

### Node.js

```bash
npm install
npm run manual
npm run json2csv
```

### Java

```bash
mvn compile
mvn exec:java -Dexec.mainClass="JsonToCsv"
```

The `pom.xml` uses Java 17, Jackson 2.17.2, and Apache Commons CSV 1.11.0.

## Notes

- Every script writes `output_*.csv` files next to the source files
  (or prints to stdout for the Node examples).
- `convert_json_stream.py` needs `ijson` because it parses the input
  incrementally; the standard library `json` module loads the whole
  document first.
- `convert_json_json2csv.mjs` uses `unwind: "orders"` to turn the
  `orders` array into one CSV row per element.
