# Data Pipeline Design Document Template — Companion

Companion files for the doc [Data Pipeline Design Document Template](https://stackpractices.com/docs/data-pipeline-design-document-template/).

## Contents

| Path | Purpose |
|------|---------|
| `template/pipeline-design-document-template.md` | Blank, fill-in version of the design document — copy it next to your pipeline code |
| `dbt/models/int_orders_dedup.sql` | Incremental dedup model (ROW_NUMBER per `order_id`) |
| `dbt/models/int_orders_enriched.sql` | Orders + customer dimension join |
| `dbt/models/fct_order_metrics.sql` | Daily metrics mart with the corrected `is_enterprise` reference |
| `airflow/orders_etl_dag.py` | Airflow 2.x DAG skeleton matching the doc's task graph |

## Notes

- `fct_order_metrics.sql` reads `is_enterprise` directly from
  `int_orders_enriched` — the column was added by the enrich join, so there is
  no `dim_customers` alias in scope at that step.
- `orders_etl_dag.py` is a skeleton: `extract_orders_from_api` raises
  `NotImplementedError` until you fill in the extraction logic from the source
  table (pagination, OAuth2, retry policy).
- The blank template keeps the 10-section structure: sources, staging,
  transforms, sinks, orchestration, error handling, monitoring, quality
  checks, and operational procedures.
