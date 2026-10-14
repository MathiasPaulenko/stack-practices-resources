# dbt Model Transformations — Companion Project

Minimal runnable dbt Core project accompanying the StackPractices recipe:
<https://stackpractices.com/recipes/python-dbt-model-transformations/>

## Contents

| Path | What it shows |
|------|---------------|
| `dbt_project.yml` | Project config with per-folder materializations (staging=view, marts=table, fct_orders=incremental) |
| `profiles.yml.example` | Connection template with `env_var()` and dev/prod targets |
| `models/staging/` | Source declarations with freshness + column tests, `stg_orders`, `stg_customers` |
| `models/marts/` | `fct_orders` incremental (unique_key + merge), `dim_customers`, schema tests |
| `macros/` | `cents_to_dollars` Jinja macro |
| `snapshots/` | SCD Type 2 snapshot with timestamp strategy |
| `tests/` | Singular test asserting no negative amounts |
| `dag_dbt.py` | Airflow DAG (`schedule=` API, Airflow ≥2.4) running `dbt build` |

## Run

```bash
pip install dbt-core dbt-postgres   # or dbt-snowflake / dbt-bigquery
cp profiles.yml.example ~/.dbt/profiles.yml   # then edit credentials
export DB_PASSWORD=...
dbt debug          # verify the connection
dbt build          # run models + tests in DAG order
dbt docs generate && dbt docs serve
```

`dbt snapshot` runs the SCD-2 snapshot separately from `dbt build`.
