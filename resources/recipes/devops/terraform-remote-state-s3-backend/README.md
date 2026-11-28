# Store Terraform Remote State in S3 with Locking

Companion code for the StackPractices recipe:
<https://stackpractices.com/recipes/terraform-remote-state-s3-backend/>

## What's here

- `bootstrap.tf` — one-time setup that creates the S3 state bucket with versioning, SSE-S3 encryption, public access blocked, and `prevent_destroy`. Apply it from a separate root module before anything else.
- `backend.tf` — S3 backend block with native locking (`use_lockfile = true`, Terraform >= 1.10) plus migration notes for `dynamodb_table` setups.
- `environments.tf` — per-environment `key` strategy (commented examples) and the workspaces alternative.

## Usage

```bash
# 1. Bootstrap the bucket (separate module, local state)
terraform init && terraform apply   # in the bootstrap module

# 2. Wire the backend in your root module, then
terraform init -migrate-state       # first time
terraform plan && terraform apply
```

Prefer OIDC (`aws-actions/configure-aws-credentials` with `role-to-assume`)
over static access keys in CI.
