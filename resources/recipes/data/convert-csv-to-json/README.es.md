# Convertir CSV a JSON — ejemplos companion

Esta carpeta contiene ejemplos ejecutables para la receta de StackPractices
[Convertir CSV a JSON](https://stackpractices.com/es/recipes/convert-csv-to-json/).

## Archivos

| Archivo | Descripción |
| --- | --- |
| `data/sample.csv` | CSV pequeño con columnas tipadas (número, booleano, fecha) |
| `convert_csv_std.py` | Versión con librería estándar de Python (`csv.DictReader` + `json`) |
| `convert_csv_pandas.py` | Versión con pandas y casteo de tipos y fechas |
| `requirements.txt` | Dependencias de Python |
| `convert_csv_csv_parse.mjs` | Versión streaming en Node con `csv-parse` |
| `convert_csv_papaparse.mjs` | Versión Node/browser con `PapaParse` |
| `package.json` | Dependencias y scripts de Node |
| `pom.xml` | Proyecto Maven para los ejemplos de Java |
| `src/main/java/CsvToJson.java` | Versión Java con Jackson CSV |
| `src/main/java/CsvToJsonCommons.java` | Versión Java con Apache Commons CSV |

## Cómo ejecutar los ejemplos

### Python

```bash
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
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

El `pom.xml` usa Java 17, Jackson 2.17.2 y Apache Commons CSV 1.11.0.
