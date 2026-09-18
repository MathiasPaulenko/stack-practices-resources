# Extracción Segura de Zips — Código complementario

Versión ejecutable de los helpers de validación de la receta
[Extraer Archivos Zip de Forma Segura con Python](https://stackpractices.com/es/recipes/python-zip-file-extraction/)
en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `safe_extract.py` | `validate_zip` (chequeos de cantidad, tamaño y paths sospechosos), `safe_extract` (guarda de path traversal vía `relative_to`), `check_duplicates`, `quarantine_zip`, y una suite `unittest` que cubre archivos normales, de traversal, con path absoluto, sobredimensionados y con entradas duplicadas |

## Requisitos

- Python 3.10+ — sin dependencias externas.

## Uso

```python
from safe_extract import safe_extract, validate_zip

validate_zip("upload.zip", max_files=1000, max_total_size_mb=500)
count = safe_extract("upload.zip", "output_dir")
```

## Notas

- `is_safe_path` usa `Path.relative_to` (Python 3.9+) en vez de un chequeo
  de strings con `startswith`, así que funciona correctamente con los
  separadores de Windows y resuelve symlinks antes de comparar.
- La validación ocurre antes de escribir un solo byte a disco: un archivo
  rechazado deja el directorio destino intacto.
- Pon en cuarentena los archivos rechazados en vez de eliminarlos si
  necesitas la evidencia para respuesta a incidentes.
