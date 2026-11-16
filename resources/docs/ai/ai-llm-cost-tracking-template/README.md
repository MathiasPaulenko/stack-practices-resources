# LLM Cost Tracking Template — Companion Resources

Companion files for the [AI LLM Cost Tracking Template](https://stackpractices.com/docs/ai-llm-cost-tracking-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `budget_config.yaml` | YAML | Monthly budget, alert thresholds (50/75/90/100%), per-feature budgets, per-tier user limits |
| `llm_cost_monitor.py` | Python | Reference monitor: aggregates spend per day/feature, fires threshold alerts, exits non-zero on throttle |
| `schema.sql` | SQL | Postgres tables for the raw per-request log and the daily rollup, with the indexes that matter |
| `llm-cost-report-template.md` | Markdown | Monthly report skeleton: summary, cost by feature/model, top users, actions, recommendations |

## Quick start

### 1. Create the tables

```bash
psql -d your_db -f schema.sql
```

### 2. Tune the budget config

Edit `budget_config.yaml`: your real monthly budget, the recipients, and which features are safe to disable at 100%.

### 3. Run the monitor

Export each LLM call as a JSONL line (see the per-request log schema in the template) and run:

```bash
pip install pyyaml
python llm_cost_monitor.py --config budget_config.yaml --log usage.jsonl
```

It prints the budget check (utilization + alerts to fire) and the daily report. Exit code is `1` when the 100% throttle threshold trips — wire that into your scheduler or alerting. Hourly cadence is right for most workloads.

### 4. Fill the monthly report

Copy `llm-cost-report-template.md` each month and fill every `[placeholder]` from the rollup table.

## Adapt before production

1. Update the pricing table in the template before trusting any numbers — model prices go stale fast.
2. Decide which features are non-critical *now*; the `disabled_features` list is not the moment to brainstorm.
3. Route `notify` alerts somewhere humans actually read — an unmonitored threshold is decoration.
