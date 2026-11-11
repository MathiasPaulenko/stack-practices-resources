# FinOps — Cloud Cost Optimization

Companion resources for the [FinOps guide](https://stackpractices.com/guides/finops-guide/)
on StackPractices.

## Files

| File | Description |
|------|-------------|
| `cost_anomaly_detection.py` | Daily Cost Explorer check: compares yesterday's spend to the 30-day average and reports the top service movers when the threshold is exceeded |
| `tagging_policy.tf` | Terraform module that enforces mandatory cost-allocation tags (Owner, Environment, Project, CostCenter, ManagedBy) with validation |
| `saas_optimization_example.md` | The worked example from the guide: how a $50K/month AWS bill gets cut 30% across right-sizing, reservations, S3 lifecycle, Spot, and RDS |

## Usage

```bash
# Anomaly detection — requires AWS credentials with ce:GetCostAndUsage
pip install boto3
python cost_anomaly_detection.py --threshold 1.20
```

```hcl
# Tagging module
module "tags" {
  source      = "./tagging_policy"
  team_email  = "platform@example.com"
  environment = "production"
  project     = "billing"
  cost_center = "CC-1234"
}
```

## Notes

- The anomaly script's exit code is `1` on anomaly — wire it to Slack/PagerDuty
  in your scheduler rather than polling stdout.
- Tune `--threshold` down (e.g. `1.10`) for stable workloads, up for spiky ones.
