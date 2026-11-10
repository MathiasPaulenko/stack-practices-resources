# ETL Extract-Transform-Load — Recursos del repositorio companion

Companion ejecutable de [Patrón ETL Extract-Transform-Load](https://stackpractices.com/es/patterns/etl-extract-transform-load-pattern/) en StackPractices.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `etl_pipeline.py` | Clase `ETLPipeline`: extracción → staging → transformación → carga delete+insert. Funciona con cualquier engine de SQLAlchemy. |
| `incremental_etl.py` | `IncrementalETL`: extracción con high-water mark persistida en `watermarks.json`. |
| `etl_customers.sql` | Las mismas tres fases en SQL puro (PostgreSQL 15+, usa `MERGE`). |
| `etl_dag.py` | DAG de Airflow que orquesta las fases del pipeline (Airflow 2.4+, requiere el provider de postgres). |
| `CustomerEtlJob.java` | Job de referencia en Spring Batch 5: `JdbcCursorItemReader` / `ItemProcessor` / `JdbcBatchItemWriter` con upsert MERGE, más las clases `Customer` y `CustomerRowMapper` que el snippet del artículo referencia. |
| `demo.py` | Corrida de punta a punta sobre SQLite: siembra datos, corre el pipeline dos veces para probar idempotencia y luego una extracción incremental. |
| `test_etl_pipeline.py` | Suite pytest que cubre la corrida completa, el nombrado de tablas de staging, las re-corridas idempotentes y los watermarks incrementales. |

## Inicio rápido

```bash
pip install pandas sqlalchemy pytest
python demo.py          # corrida de punta a punta sobre SQLite
pytest test_etl_pipeline.py -v
```

`demo.py` crea `demo_source.db`, `demo_staging.db`, `demo_warehouse.db` y `demo_watermarks.json` en el directorio de trabajo; se pueden borrar después.

## Notas

- `etl_pipeline.py` usa un upsert delete+insert portable (`IN` con bind expansible) para correr en SQLite, Postgres y MySQL. El artículo muestra la variante específica de Postgres `id = ANY(:ids)`.
- `etl_customers.sql` y `CustomerEtlJob.java` están en dialecto PostgreSQL; adapta la sintaxis del upsert para MySQL (`INSERT ... ON DUPLICATE KEY UPDATE`) o SQL Server/Oracle más antiguos. El archivo Java apunta a Spring Batch 5 (`JobRepository` + `PlatformTransactionManager`); el artículo también muestra la variante con `*BuilderFactory` de Batch 4.
- El DAG espera conexiones de Airflow llamadas `source_db`, `staging_db` y `warehouse_db`.
