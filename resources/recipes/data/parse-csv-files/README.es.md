# Analizar Archivos CSV — Archivos complementarios

Archivos complementarios de [Analizar Archivos CSV](https://stackpractices.com/es/recipes/parse-csv-files/) en StackPractices.

## Contenido

- `parse_csv.py` — `parse_rows`, `parse_dicts`, `parse_dicts_strict` (saltar y registrar filas malformadas), `sniff_delimiter` y `stream_sum` (variante para archivos grandes).
- `sample.csv` — CSV estándar con un campo entrecomillado que contiene una coma.
- `sample_bom.csv` — archivo UTF-8 con BOM, el caso típico de exportación de Excel.
- `sample_semicolon.csv` — archivo delimitado por `;` al estilo europeo.
- `test_parse_csv.py` — suite pytest que cubre todos los helpers. Ejecuta: `pytest test_parse_csv.py -v`.

## Qué mirar

- `utf-8-sig` en todos lados — el detalle que evita el bug de la primera columna `\ufeffname`.
- `test_quoted_field_with_comma` es la razón por la que `split(',')` no es confiable: el campo `b@x.com, inc` debe sobrevivir como una sola celda.
- `sniff_delimiter` + `DictReader` maneja archivos cuyo delimitador no controlas.
