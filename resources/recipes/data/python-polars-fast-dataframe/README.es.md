# Polars: DataFrames de alto rendimiento en Python

Código de acompañamiento para la [receta de Polars para DataFrames rápidos](https://stackpractices.com/es/recipes/python-polars-fast-dataframe/) en StackPractices.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `polars_basics.py` | Operaciones básicas de DataFrame: select, filter, group-by, join, `when/then`, `replace_strict`, window functions, pivot |
| `lazy_pipeline.py` | Lazy evaluation: `scan_*`, query plans con `explain()`, streaming engine con `collect(engine="streaming")` |
| `pandas_interop.py` | Conversiones entre pandas, Polars y PyArrow |
| `test_polars_examples.py` | Tests unitarios de todos los ejemplos (pytest) |

## Setup

```bash
pip install "polars>=1.0" pandas pyarrow pytest
```

Los ejemplos van sobre `polars>=1.0`. Cambios de API de 1.0 usados aquí:
`pivot(on=...)` (antes `columns=`) y `collect(engine="streaming")` (antes `streaming=True`).

## Ejecutar los ejemplos

```bash
python polars_basics.py
python lazy_pipeline.py
python pandas_interop.py
```

## Ejecutar los tests

```bash
pytest test_polars_examples.py -v
```
