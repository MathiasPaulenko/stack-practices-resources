# Convertir JSON a CSV — ejemplos complementarios

Esta carpeta contiene ejemplos ejecutables para la receta de StackPractices
[Convertir JSON a CSV](https://stackpractices.com/es/recipes/convert-json-to-csv/).

## Archivos

| Archivo | Descripción |
| --- | --- |
| `data/sample.json` | Array JSON plano de objetos |
| `data/sample_nested.json` | JSON anidado con objetos y un campo array |
| `data/sample.jsonl` | JSON Lines (un objeto por línea) |
| `convert_json_std.py` | Versión con la stdlib de Python (`csv.DictWriter`) y cabeceras por unión de claves |
| `convert_json_pandas.py` | Versión con pandas y `json_normalize` para objetos anidados |
| `convert_json_stream.py` | Versión con ijson en streaming para archivos mayores que la memoria |
| `convert_jsonl_std.py` | JSON Lines a CSV con la stdlib |
| `requirements.txt` | Dependencias de Python |
| `convert_json_manual.mjs` | Versión de Node.js sin dependencias |
| `convert_json_json2csv.mjs` | Versión de Node.js con `@json2csv` (unwind de arrays) |
| `package.json` | Dependencias y scripts de Node |
| `pom.xml` | Proyecto Maven para el ejemplo de Java |
| `src/main/java/JsonToCsv.java` | Versión de Java con Jackson + Apache Commons CSV |

## Cómo ejecutar los ejemplos

### Python

```bash
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
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

El `pom.xml` usa Java 17, Jackson 2.17.2 y Apache Commons CSV 1.11.0.

## Notas

- Cada script escribe archivos `output_*.csv` junto a los fuentes
  (o imprime en stdout en los ejemplos de Node).
- `convert_json_stream.py` necesita `ijson` porque parsea la entrada
  de forma incremental; el módulo `json` de la stdlib carga el documento
  entero primero.
- `convert_json_json2csv.mjs` usa `unwind: "orders"` para convertir el
  array `orders` en una fila CSV por elemento.
