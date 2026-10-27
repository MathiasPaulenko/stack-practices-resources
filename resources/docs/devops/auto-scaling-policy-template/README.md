# Auto-Scaling Policy Template — Companion Resources

Runnable assets for the [Auto-Scaling Policy Template](https://stackpractices.com/docs/auto-scaling-policy-template/) on StackPractices.

## Files

| File | Description |
|------|-------------|
| `auto-scaling-policy-template.md` | The copy-ready policy document — fill the `<Service Name>` header and tune the thresholds |
| `autoscaling.tf` | Terraform: AWS Auto Scaling Group with scale-up/scale-down policies and CloudWatch alarms |
| `hpa.yaml` | Kubernetes HorizontalPodAutoscaler (autoscaling/v2) with CPU, memory, and custom RPS metrics |
| `scaling-events-example.txt` | Sample scaling-event log format for dashboards and audits |

## Usage

1. Copy `auto-scaling-policy-template.md` into your team's docs and fill in service metadata.
2. Adapt `autoscaling.tf` or `hpa.yaml` to your platform — pick thresholds against your measured warm-up time, not the defaults.
3. Load-test the policy in staging before enabling it in production (see the doc's *Adopting This Policy* section).
