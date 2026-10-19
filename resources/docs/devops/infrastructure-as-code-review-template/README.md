# Infrastructure as Code Review Template — Companion

Runnable versions of the examples in [Infrastructure as Code Review Template](https://stackpractices.com/docs/infrastructure-as-code-review-template/).

## Files

| File | Purpose |
|------|---------|
| `terraform-review.yml` | GitHub Actions workflow — Checkov SARIF scan + `terraform plan` posted as a PR comment |
| `aws_require_tags.py` | Custom Checkov policy requiring `CostCenter` and `Environment` tags on AWS resources |
| `infrastructure_test.go` | Terratest test that applies a VPC module and asserts on its outputs |
| `drift_detector.py` | Scheduled drift check (`plan -detailed-exitcode`) with email alerting |

## Usage

```bash
# Custom Checkov policy
checkov -d terraform/ --external-checks-dir . --framework terraform

# Terratest (needs AWS credentials)
cd test && go test -v -timeout 30m

# Drift detector (schedule with cron or a CI schedule trigger)
python drift_detector.py
```

## Requirements

- Terraform >= 1.7, Checkov, Go >= 1.21 (for Terratest)
- AWS credentials for `terraform plan` / Terratest
