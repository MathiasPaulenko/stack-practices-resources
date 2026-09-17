# Compute Resource Consolidation — Companion Tools

Runnable companion scripts for the
[Compute Resource Consolidation Pattern](https://stackpractices.com/patterns/compute-resource-consolidation-pattern/)
on StackPractices.

## Contents

| File | Purpose |
|------|---------|
| `workload-analyzer.py` | Evaluates which workload pairs are safe to consolidate based on average usage and peak-hour overlap |
| `spot-consolidation.py` | Groups batch workloads by execution window and plans one spot instance per window (`--dry-run` supported) |
| `workloads.example.json` | Example workload dataset usable with both scripts |

## Usage

```bash
# Which workloads can share a node?
python workload-analyzer.py workloads.example.json

# How do batch jobs group into spot-instance windows? (no AWS calls)
python spot-consolidation.py workloads.example.json --dry-run
```

## Requirements

- Python 3.10+
- `boto3` only for real spot requests (not needed for `--dry-run`)

Both scripts exit non-zero on invalid input so they can gate CI jobs.
