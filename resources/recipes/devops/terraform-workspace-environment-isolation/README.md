# Isolate Environments with Terraform Workspaces

Runnable Terraform configuration for environment isolation with CLI workspaces: S3 backend with native lockfile, per-workspace `env_config` locals, and per-environment `.tfvars`.

## Files

- `backend.tf` — S3 backend with `use_lockfile` (Terraform >= 1.10). One `key` for all workspaces; states land under `env:/<workspace>/`.
- `environments.tf` — `env_config` map keyed by `terraform.workspace` plus a commented conditional resource example.
- `dev.tfvars` / `staging.tfvars` / `production.tfvars` — per-environment variable files.

## Usage

```bash
terraform init
terraform workspace new dev
terraform workspace new production

terraform workspace select dev
terraform apply -var-file="dev.tfvars"

terraform workspace select production
terraform apply -var-file="production.tfvars"
```

## Notes

- Do not interpolate `terraform.workspace` in the backend block — it is not available at init time. The `env:` prefix isolates each workspace automatically; customize it with `workspace_key_prefix`.
- Before deleting a workspace, destroy its resources first: `terraform destroy`, then `terraform workspace select default && terraform workspace delete <name>`.
- Source article: https://stackpractices.com/recipes/terraform-workspace-environment-isolation/
