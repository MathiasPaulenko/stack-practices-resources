# Validación de Schemas de DataFrame con Pandera — Recurso Companion

Código companion de la receta de StackPractices [Validar schemas de DataFrame con Pandera](https://stackpractices.com/es/recipes/python-data-validation-pandera/).

## Contenidos

- `schema_validation.py` — DataFrameSchema básico, DataFrameModel basado en clases, checks personalizados de email y herencia de schemas.
- `pipeline_validation.py` — Validación de input/output en límites del pipeline, manejo de errores con lazy validation y validación con decoradores.
- `test_validation.py` — Tests de pytest cubriendo datos válidos, inválidos, strict mode, coerción y validación de pipeline.
- `meta.json` — Metadata del recurso.

## Ejecución

```bash
pip install pandera pandas pytest
python -m pytest test_validation.py -v
```

## Conceptos clave

- **DataFrameSchema**: schema basado en diccionarios para validación rápida.
- **DataFrameModel**: schema basado en clases para schemas reutilizables y heredables.
- **Checks personalizados**: funciones de validación element-wise y a nivel serie.
- **Coerción**: conversión automática de tipos antes de validar.
- **Strict mode**: rechazar columnas inesperadas para detectar schema drift.
- **Lazy validation**: acumular todos los errores a la vez en vez de detenerse en el primero.
- **Validación de pipeline**: validar en los límites de entrada y salida.
- **Integración con pytest**: usar validación de schemas como gates de CI.
