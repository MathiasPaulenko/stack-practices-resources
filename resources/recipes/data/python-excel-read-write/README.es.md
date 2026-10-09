# Leer y Escribir Excel en Python (openpyxl + pandas)

Recurso complementario de [Leer y Escribir Excel en Python](https://stackpractices.com/es/recipes/python-excel-read-write/).

## Archivos

- `excel_examples.py` — todos los ejemplos de código de la recipe, ejecutables como comandos independientes.
- `requirements.txt` — dependencias de Python.

## Uso

```bash
pip install -r requirements.txt
python excel_examples.py sample        # crea sample.xlsx primero
python excel_examples.py pandas_read
python excel_examples.py pandas_write
python excel_examples.py openpyxl_format
python excel_examples.py openpyxl_read
python excel_examples.py formulas
python excel_examples.py append
python excel_examples.py large_file
```

## Ejemplos

| Comando | Descripción |
|---------|-------------|
| `sample` | Crea `sample.xlsx` con datos de ejemplo (ejecutar primero) |
| `pandas_read` | Lee una hoja y todas las hojas con `pd.read_excel` |
| `pandas_write` | Escribe una hoja y varias hojas |
| `openpyxl_format` | Reporte con estilos: rellenos, fuentes, bordes, freeze panes, autofiltro |
| `openpyxl_read` | Lee celdas y rangos con `load_workbook` |
| `formulas` | Escribe celdas con fórmulas `=SUM`/`=AVERAGE` |
| `append` | Agrega una hoja a un workbook existente con `mode="a"` |
| `large_file` | Lectura en streaming con `read_only=True` |
