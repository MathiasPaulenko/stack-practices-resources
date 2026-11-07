# Cloud Cost Optimization Guide — Companion Files

Artifacts from the [Cloud Cost Optimization program guide](https://stackpractices.com/guides/cost-optimization-cloud-guide/)
on StackPractices.

## Files

| File | What it does |
|------|--------------|
| `rightsize_report.py` | Flags underutilized instances from a metrics CSV using p95 CPU (not average). Prints DOWNSIZE vs TERMINATE recommendations. |
| `cost-inventory.csv` | The worked-example inventory from the guide — a per-service spend breakdown you can adapt for your own Phase 1 audit. |

## Quick start

```bash
# 1. Export 30 days of p95 metrics into a CSV with columns:
#    instance_id, instance_type, cpu_p95, memory_p95

# 2. Run the analyzer
python rightsize_report.py instance_metrics.csv
python rightsize_report.py instance_metrics.csv --cpu-threshold 30

# 3. Copy cost-inventory.csv and fill in your own service breakdown
```

## Requirements

- Python 3.9+ (stdlib only — no pandas needed)
- Metrics exported from CloudWatch, Azure Monitor, or your observability stack

## Source

- Guide EN: https://stackpractices.com/guides/cost-optimization-cloud-guide/
- Guide ES: https://stackpractices.com/es/guides/cost-optimization-cloud-guide/
