# Guía de pipelines ETL — Código complementario

Complemento ejecutable de la guía [Pipelines ETL: Extract, Transform, Load para Ingenieros](https://stackpractices.com/es/guides/etl-pipeline-guide/).

El pipeline central usa `sqlite3` para correr en cualquier parte; las mismas formas funcionan en Postgres con placeholders `%s` y `psycopg2`.

## Archivos

| Archivo | Propósito |
|---|---|
| `etl_pipeline.py` | `IncrementalExtractor` (watermark, orden correcto), `DataTransformer` con `ValidationError`, `UpsertLoader` — las versiones corregidas de las clases de la guía |
| `demo.py` | Ejecución completa: 3 filas extraídas, la segunda corrida mueve 0 filas (watermark), una actualización upstream carga solo la fila cambiada |
| `test_etl_pipeline.py` | Suite pytest: extracción incremental, rechazo del validador, orden de transformaciones, idempotencia del upsert |
| `daily_etl_dag.py` | DAG de referencia para Airflow 2.x (`schedule=`, archivos de staging en S3 entre tareas, upsert vía tabla temporal) |
| `scd-type2.sql` | DDL de Slowly Changing Dimension Tipo 2 + sentencias de expiración/inserción (PostgreSQL) |

## Inicio rápido

```bash
python demo.py          # demo completa sobre sqlite en memoria
python -m pytest -q     # 4 tests
```

Salida esperada de la demo:

```
run 1: extracted=3 loaded=3
run 2: extracted=0 loaded=0
warehouse: 3 rows, total=63.0
run 3 (after update): extracted=1
order 1 now: qty=9 total=81.0
```

## Notas

- `daily_etl_dag.py` es un archivo de referencia: necesita un entorno Airflow 2.x real con conexiones `production_db`, `aws_default` y `warehouse`. No corre de forma independiente.
- La extracción por watermark ordena por la columna del watermark (y luego `rowid`): la guía explica por qué ordenar solo por id puede saltar filas cuando un lote se trunca.
