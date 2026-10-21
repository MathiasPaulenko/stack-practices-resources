# Importar Datos desde CSV/Excel — Recursos complementarios

Scripts ejecutables para la receta [Importar Datos desde CSV/Excel](https://stackpractices.com/es/recipes/import-csv-excel/) en StackPractices.

## Contenido

| Archivo | Descripción |
|---------|-------------|
| `import_csv.py` | Importación CSV en streaming: detección de encoding, sniffing de delimitador, validación fila a fila con Pydantic, inserción por lotes en SQLite dentro de una transacción. |
| `import_csv.js` | Equivalente en Node.js con `csv-parser` y colección de errores por fila. |
| `sample-users.csv` | Archivo de muestra con casos límite: nombres con tildes, un nombre vacío, una edad inválida y una fila duplicada. |

## Uso

```bash
# Python — genera una base SQLite users.db más un informe JSON
python import_csv.py sample-users.csv users.db

# Node — imprime el informe de válidos/errores
node import_csv.js sample-users.csv
```

El archivo de muestra ejercita los fallos cubiertos en la receta: la fila 4 falla la validación (nombre vacío), la fila 5 falla (edad no numérica) y la fila 7 es un duplicado gestionado por `INSERT OR IGNORE`.

## Fuente

- Receta: https://stackpractices.com/recipes/import-csv-excel/
- Receta (ES): https://stackpractices.com/es/recipes/import-csv-excel/
