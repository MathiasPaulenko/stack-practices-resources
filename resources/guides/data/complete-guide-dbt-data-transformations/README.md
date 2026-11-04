# dbt: Models, Tests, Macros, Materializations — Companion Project

A minimal but complete dbt project covering the patterns from the
[Complete Guide to dbt Data Transformations](https://stackpractices.com/guides/complete-guide-dbt-data-transformations/).

## Contents

| File | What it shows |
| --- | --- |
| `dbt_project.yml` | Per-folder materialization and schema defaults, test config |
| `packages.yml` | `dbt_utils` + `dbt_expectations` dependencies |
| `models/staging/sources.yml` | Source declaration with freshness rules |
| `models/staging/schema.yml` | Generic tests: unique, not_null, relationships, accepted_values, `dbt_utils` expression tests |
| `models/staging/stg_orders.sql` | Staging model (rename, cast, trim — no business logic) |
| `models/intermediate/int_orders_enriched.sql` | Join + business logic between staging and marts |
| `models/marts/core/fct_orders.sql` | Incremental fact with `is_incremental()` guard |
| `macros/cents_to_dollars.sql` | Reusable Jinja macro |
| `seeds/country_codes.csv` | Static reference data loaded with `dbt seed` |
| `snapshots/snap_customers.sql` | SCD Type 2 snapshot (timestamp strategy) |
| `tests/assert_positive_revenue.sql` | Singular custom test |

## Quick start

```bash
pip install dbt-snowflake   # or dbt-bigquery / dbt-postgres / dbt-duckdb
# Configure ~/.dbt/profiles.yml with your warehouse credentials
dbt deps
dbt seed
dbt build       # run + test in DAG order
dbt snapshot
dbt docs generate && dbt docs serve
```

Requires `profiles.yml` in `~/.dbt/` — never commit credentials.
