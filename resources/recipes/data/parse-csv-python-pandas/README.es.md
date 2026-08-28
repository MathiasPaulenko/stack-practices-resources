# Leer Archivos CSV con Python y Pandas

Recurso companion para [Leer Archivos CSV con Python y Pandas](https://stackpractices.com/es/recipes/parse-csv-python-pandas/).

## Archivos

- `parse_csv_examples.py` — todos los ejemplos de código de la receta, ejecutables como funciones independientes.
- `sample.csv` — dataset de ventas de ejemplo con 10 filas para testing.
- `requirements.txt` — dependencias de Python.

## Uso

```bash
pip install -r requirements.txt
python parse_csv_examples.py basic
python parse_csv_examples.py pandas_read
python parse_csv_examples.py filter
python parse_csv_examples.py chunked
python parse_csv_examples.py encoding
python parse_csv_examples.py typed
python parse_csv_examples.py memory
```

## Ejemplos

| Comando | Descripción |
|---------|-------------|
| `basic` | Parseo CSV con el módulo `csv` del stdlib |
| `pandas_read` | Lectura CSV con `pd.read_csv` |
| `filter` | Filtrado, agrupación y exportación |
| `chunked` | Procesamiento por chunks para archivos grandes |
| `encoding` | Manejo de problemas de encoding (UTF-8, latin-1, cp1252) |
| `typed` | Especificación explícita de dtype |
| `memory` | Optimización de memoria con dtype y usecols |
