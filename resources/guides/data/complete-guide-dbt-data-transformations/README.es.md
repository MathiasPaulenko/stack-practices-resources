# dbt: Modelos, Tests, Macros y Materializaciones — Proyecto de ejemplo

Un proyecto dbt mínimo pero completo con los patrones de la
[Guía Completa de dbt para Transformaciones de Datos](https://stackpractices.com/es/guides/complete-guide-dbt-data-transformations/).

## Contenido

| Archivo | Qué muestra |
| --- | --- |
| `dbt_project.yml` | Defaults de materialización y esquema por carpeta, config de tests |
| `packages.yml` | Dependencias `dbt_utils` + `dbt_expectations` |
| `models/staging/sources.yml` | Declaración de sources con reglas de frescura |
| `models/staging/schema.yml` | Tests genéricos: unique, not_null, relationships, accepted_values, tests `dbt_utils` |
| `models/staging/stg_orders.sql` | Modelo staging (renombrar, castear, trim — sin lógica de negocio) |
| `models/intermediate/int_orders_enriched.sql` | Join + lógica de negocio entre staging y marts |
| `models/marts/core/fct_orders.sql` | Fact incremental con guard `is_incremental()` |
| `macros/cents_to_dollars.sql` | Macro Jinja reutilizable |
| `seeds/country_codes.csv` | Datos de referencia estáticos cargados con `dbt seed` |
| `snapshots/snap_customers.sql` | Snapshot SCD tipo 2 (estrategia timestamp) |
| `tests/assert_positive_revenue.sql` | Test singular personalizado |

## Inicio rápido

```bash
pip install dbt-snowflake   # o dbt-bigquery / dbt-postgres / dbt-duckdb
# Configura ~/.dbt/profiles.yml con las credenciales del warehouse
dbt deps
dbt seed
dbt build       # run + test en orden del DAG
dbt snapshot
dbt docs generate && dbt docs serve
```

Requiere `profiles.yml` en `~/.dbt/` — nunca commitees credenciales.
