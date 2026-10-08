# Construir un Pipeline ETL con pandas y Parquet

Código ejecutable que acompaña a la receta de StackPractices:
[Construir un Pipeline ETL con pandas y Parquet](https://stackpractices.com/es/recipes/python-pandas-etl-pipeline/)

Un pipeline extract-transform-load completo en un solo archivo: lee fuentes
CSV/JSON, coacciona tipos, valida la calidad de los datos y escribe Parquet
particionado con compresión `snappy`. Incluye lógica de reintentos para
fuentes inestables, carga incremental con deduplicación y validación de
esquema.

## Contenido

| Archivo | Qué hace |
|---|---|
| `etl_pipeline.py` | Pipeline completo: `extract_csv`, `extract_json`, `extract_with_retry`, `extract_and_merge`, `transform`, `transform_with_validation`, `enforce_schema`, `load_partitioned`, `load_incremental`, `run_pipeline_safe` |
| `requirements.txt` | `pandas` + `pyarrow` |

## Instalación y ejecución

```bash
pip install -r requirements.txt
python etl_pipeline.py
```

El script genera un `data/raw/orders.csv` de muestra (con un monto negativo,
un valor numérico inválido y un ID duplicado para que veas la validación en
acción), ejecuta el pipeline y escribe la salida particionada en
`data/processed/orders/year=*/month=*/`.

Para leer una partición de vuelta:

```python
import pandas as pd
df = pd.read_parquet("data/processed/orders/year=2025/month=02")
```

## Notas

- `errors="coerce"` convierte valores inválidos en `NaN` en vez de lanzar
  error — combinado con el dtype nullable `Int64` para que los enteros
  faltantes sobrevivan al cast.
- Los reintentos envuelven solo `extract`: los errores de transformación son
  deterministas, los de E/S no.
- Cambia `compression="snappy"` por `"zstd"` cuando importe más el coste de
  almacenamiento que la velocidad de escritura.
