# Transformaciones con modelos dbt — Proyecto complementario

Proyecto mínimo ejecutable de dbt Core que acompaña a la receta de StackPractices:
<https://stackpractices.com/es/recipes/python-dbt-model-transformations/>

## Contenido

| Ruta | Qué muestra |
|------|-------------|
| `dbt_project.yml` | Config del proyecto con materializaciones por carpeta (staging=view, marts=table, fct_orders=incremental) |
| `profiles.yml.example` | Plantilla de conexión con `env_var()` y targets dev/prod |
| `models/staging/` | Declaración de sources con freshness + tests de columnas, `stg_orders`, `stg_customers` |
| `models/marts/` | `fct_orders` incremental (unique_key + merge), `dim_customers`, tests de esquema |
| `macros/` | Macro Jinja `cents_to_dollars` |
| `snapshots/` | Snapshot SCD tipo 2 con estrategia timestamp |
| `tests/` | Test singular que verifica montos no negativos |
| `dag_dbt.py` | DAG de Airflow (API `schedule=`, Airflow ≥2.4) que corre `dbt build` |

## Ejecutar

```bash
pip install dbt-core dbt-postgres   # o dbt-snowflake / dbt-bigquery
cp profiles.yml.example ~/.dbt/profiles.yml   # después editá las credenciales
export DB_PASSWORD=...
dbt debug          # verifica la conexión
dbt build          # corre modelos + tests en orden de DAG
dbt docs generate && dbt docs serve
```

`dbt snapshot` corre el snapshot SCD-2 por separado de `dbt build`.
