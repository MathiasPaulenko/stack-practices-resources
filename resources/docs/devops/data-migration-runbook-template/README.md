# Data Migration Runbook — Companion Resources

Companion files for the [Data Migration Runbook Template](https://stackpractices.com/docs/data-migration-runbook-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `migration-runbook.md` | Markdown | Ready-to-adapt runbook: pre-migration checklist, strategy table, dry run, execution, validation, and rollback |
| `validate-migration.sh` | Bash | Row-count comparison between source and target PostgreSQL databases, table by table |

## Quick start

### 1. Copy the runbook

```bash
cp migration-runbook.md oncall/migrations/$(date +%Y-%m-%d)-my-migration.md
```

Fill in every `______` blank: hostnames, row counts, thresholds, owners, and the decision record.

### 2. Run the validation script

```bash
export DB_NAME=mydb DB_USER=readonly
export TABLES="orders users payments"

./validate-migration.sh \
  --source source.db.internal \
  --target target.db.internal
```

The script prints a per-table comparison and exits non-zero if any count mismatches — wire it into your dry-run and post-migration validation steps.

## Rehearse before production

1. Run the dry-run section against a staging copy at production scale.
2. Record actual durations in the runbook — they become the baseline for the next estimate.
3. Rehearse the rollback steps at least once before the production window.

See the [full guide on StackPractices](https://stackpractices.com/docs/data-migration-runbook-template/) for strategy selection, troubleshooting, and rollback criteria.
