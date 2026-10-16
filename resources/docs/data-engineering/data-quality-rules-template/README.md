# Data Quality Rules Template — Companion Files

Files that back the [Data Quality Rules Template](https://stackpractices.com/docs/data-quality-rules-template/) doc on StackPractices. Copy them into your project and adapt the dataset, columns, and thresholds.

## Contents

| Path | What it is |
|------|------------|
| `template/data-quality-rules-template.md` | The full rules document for `fct_orders`: 28 rules across completeness, consistency, accuracy, timeliness, uniqueness, and validity, with severity and action-on-failure per rule. |
| `dbt/schema.yml` | dbt model tests: `not_null`, `unique`, `accepted_values`, `relationships`, and `dbt_utils.expression_is_true` checks including model-level conditional rules. |
| `dbt/tests/assert_row_count_range.sql` | Custom dbt test that fails when row count falls outside an expected range. |
| `dbt/tests/assert_data_freshness.sql` | Custom dbt test that fails when the newest `_ingested_at` is more than 24 hours old. |
| `great-expectations/fct_orders_suite.py` | Great Expectations suite: nulls, uniqueness, regex, enum sets, ranges, conditional cross-column rule, and table row count. |

## How to use

1. Copy `template/data-quality-rules-template.md` into your docs folder and replace `fct_orders`, the columns, and the thresholds with your own dataset.
2. Adapt `dbt/schema.yml` to your dbt model and place it next to the model file. Custom tests go under your project's `tests/` directory.
3. Adapt `great-expectations/fct_orders_suite.py` to your checkpoint or validation workflow. It requires `great_expectations` installed and a configured Data Context.
4. Assign severities honestly: critical blocks the pipeline, warnings log and proceed. A suite where everything is critical trains the team to ignore alerts.

Source doc: https://stackpractices.com/docs/data-quality-rules-template/
