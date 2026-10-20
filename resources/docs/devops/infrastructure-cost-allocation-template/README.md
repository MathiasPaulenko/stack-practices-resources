# Cloud Cost Allocation Template — Companion Kit

Reusable artifacts extracted from the [Cloud Cost Allocation Template](https://stackpractices.com/docs/infrastructure-cost-allocation-template/) doc on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `aws-tag-policy.yaml` | AWS Organization tag policy enforcing required cost tags at creation |
| `terraform-tag-enforcement.hcl` | Terraform module snippet applying mandatory baseline tags + CI validation hook |
| `kubecost-allocation.yaml` | Kubecost config for namespace/label allocation and shared cost splitting |
| `detect-untagged-resources.py` | Weekly scan: finds untagged AWS resources and reports their weekly cost |
| `monthly-cost-report.txt` | Fillable monthly allocation report format for finance |
| `cost-allocation-worksheet.csv` | Resource-level allocation worksheet (import to Sheets/Excel) |

## Usage

1. Deploy `aws-tag-policy.yaml` (or the Terraform equivalent) before allocating anything — retroactive tagging never fully closes the gap.
2. Configure Kubecost with `kubecost-allocation.yaml` if Kubernetes is a significant share of spend.
3. Schedule `detect-untagged-resources.py` weekly; route untagged spend to a quarantine cost center.
4. Fill `cost-allocation-worksheet.csv` per resource, then produce the monthly report from `monthly-cost-report.txt`.

See the doc for the full model, split rules, and the rollout playbook.
