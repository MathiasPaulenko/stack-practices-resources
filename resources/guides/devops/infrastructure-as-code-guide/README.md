# Infrastructure as Code — Companion Code

Runnable companion for the [Infrastructure as Code guide](https://stackpractices.com/guides/infrastructure-as-code-guide/) on StackPractices.

## What's inside

- `modules/vpc/` — a parameterized VPC module: private + public subnets across three AZs, internet gateway and public route table
- `environments/` — directory-per-environment layout (`dev`, `staging`, `production`), each with its own S3 backend using native lockfile (`use_lockfile = true`, Terraform ≥ 1.10)
- `.github/workflows/iac.yml` — the plan-on-PR / apply-on-merge pipeline with `fmt`, `validate` and Checkov
- `scripts/check-drift.sh` — scheduled drift check using `terraform plan -detailed-exitcode` across environments

## Usage

```bash
cd environments/dev
terraform init   # requires the S3 backend bucket to exist
terraform plan
```

Each environment only holds variables, the backend, and module calls — all resource logic lives in `modules/`.

## Related

- Guide (EN): https://stackpractices.com/guides/infrastructure-as-code-guide/
- Guide (ES): https://stackpractices.com/es/guides/infrastructure-as-code-guide/
