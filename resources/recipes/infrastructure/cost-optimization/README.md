# Cloud Cost Optimization — Companion Files

Executable artifacts from the [Cloud Cost Optimization recipe](https://stackpractices.com/recipes/cost-optimization/)
on StackPractices. Each file is copy-paste runnable against a real AWS account.

## Files

| File | What it does |
|------|--------------|
| `find-orphaned-resources.sh` | Weekly sweep for unattached EBS volumes, unassociated Elastic IPs, snapshots older than 90 days, stopped instances, and unattached ENIs. Read-only. |
| `budget-alerts.tf` | AWS Budgets: total monthly + per-service (EC2) budgets with email alerts at 80% actual, 100% actual, and 100% forecasted. |
| `dev-schedule.tf` | Auto Scaling scheduled actions that run dev/staging 9:00–18:00 Mon–Fri — ~73% off-hours savings. |
| `infracost-ci.yml` | GitHub Action that comments Terraform cost diffs on pull requests. |

## Quick start

```bash
# 1. See what's leaking money right now (read-only)
chmod +x find-orphaned-resources.sh
./find-orphaned-resources.sh us-east-1

# 2. Turn on budget alerts
terraform init
terraform apply -var="alert_email=finops@example.com" \
  -target=aws_budgets_budget.monthly_total

# 3. Schedule your dev ASG off-hours
terraform apply -var="asg_name=my-dev-asg" \
  -target=aws_autoscaling_schedule.dev_scale_up \
  -target=aws_autoscaling_schedule.dev_scale_down

# 4. Add infracost-ci.yml as .github/workflows/infracost.yml
#    and set the INFRACOST_API_KEY repo secret.
```

## Requirements

- AWS CLI v2 configured (`aws configure` or `AWS_PROFILE`)
- Terraform >= 1.0 for the `.tf` files
- `jq` for the sweep script
- Infracost API key for the CI workflow

## Source

- Recipe EN: https://stackpractices.com/recipes/cost-optimization/
- Recipe ES: https://stackpractices.com/es/recipes/cost-optimization/
