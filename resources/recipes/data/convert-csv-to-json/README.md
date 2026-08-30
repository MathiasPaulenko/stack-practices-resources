# Convert CSV to JSON — companion examples

This folder contains runnable examples for the StackPractices recipe
[Convert CSV to JSON](https://stackpractices.com/recipes/convert-csv-to-json/).

## Files

| File | Description |
| --- | --- |
| `data/sample.csv` | Small CSV file with typed columns (number, boolean, date string) |
| `convert_csv_std.py` | Python standard library version (`csv.DictReader` + `json`) |
| `convert_csv_pandas.py` | pandas version with type and date casting |
| `requirements.txt` | Python dependencies |
| `convert_csv_csv_parse.mjs` | Node streaming version with `csv-parse` |
| `convert_csv_papaparse.mjs` | Node/browser version with `PapaParse` |
| `package.json` | Node dependencies and scripts |
| `pom.xml` | Maven project for the Java examples |
| `src/main/java/CsvToJson.java` | Java version with Jackson CSV |
| `src/main/java/CsvToJsonCommons.java` | Java version with Apache Commons CSV |

## Running the examples

### Python

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python convert_csv_std.py
python convert_csv_pandas.py
```

### Node.js

```bash
npm install
npm run csv-parse
npm run papaparse
```

### Java

```bash
mvn compile
mvn exec:java -Dexec.mainClass="CsvToJson"
mvn exec:java -Dexec.mainClass="CsvToJsonCommons"
```

The `pom.xml` uses Java 17, Jackson 2.17.2, and Apache Commons CSV 1.11.0.
