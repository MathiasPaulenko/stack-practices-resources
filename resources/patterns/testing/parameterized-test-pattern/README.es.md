# Patrón Parameterized Test — Archivos complementarios

Archivos complementarios del [Patrón Parameterized Test](https://stackpractices.com/es/patterns/parameterized-test-pattern/) en StackPractices.

## Contenido

- `calculator.py` — `add`, `evaluate`, `format_currency`: las funciones bajo test.
- `validators.py` — `validate_email`: el ejemplo multi-parámetro.
- `test_parameterized.py` — todas las variantes parametrizadas del artículo: `parametrize` con `ids` legibles, el validador de email multi-parámetro, producto cruzado (`moneda × importe`) y un test dirigido por CSV. Ejecútalo: `pytest test_parameterized.py -v`.
- `email_cases.csv` — la tabla de casos de la variante con datos externos.

## Qué mirar

- `ids=[...]` convierte `test_to_upper[4]` en `test_to_upper[camelcase]` — el informe de fallos nombra el caso, no su número de fila.
- La tabla de `pytest.raises` muestra el mismo patrón para rutas de error: un test, una tabla de entradas inválidas.
- `_load_csv_cases` mantiene los datos junto al test pero en un archivo que alguien no desarrollador puede editar — la variante de fuente externa.
- `test_format_currency` es la trampa del producto cruzado: 2 decoradores, 16 tests. Añade una tercera dimensión y crece rápido.
