# Terraform in Production — Companion Resources

Runnable artifacts from the guide [Complete Guide to Terraform in Production](https://stackpractices.com/guides/complete-guide-terraform-production/) — the operational layer: remote state with native locking, environment isolation, drift detection, a reviewed-plan CI/CD pipeline, and policy as code.

For the VPC module referenced by `environments/production/main.tf`, see the sibling companion `resources/guides/devops/complete-guide-terraform-modules/`.

## Contents

| Path | What it is |
|---|---|
| `bootstrap/main.tf` | One-time state bucket: versioning + public access block + `prevent_destroy` |
| `environments/production/backend.tf` | S3 backend with `use_lockfile` (native locking, TF ≥ 1.10 — no DynamoDB) |
| `environments/production/main.tf` | Thin root module: provider `default_tags` + module composition |
| `environments/production/variables.tf` | Region var + sensitive `db_password` fed by `TF_VAR_` in CI |
| `policies/sentinel/require-tags.sentinel` | Mandatory tags policy (HCP Terraform/Enterprise only) |
| `policies/checks.tf` | Native `check` block alternative for OSS pipelines |
| `scripts/drift-check.sh` | Real drift detection via `plan -refresh-only` |
| `.github/workflows/terraform.yml` | Pipeline: validate → plan artifact → approval gate → `apply plan.tfplan` (OIDC, no AWS keys) |
| `.github/workflows/drift-detection.yml` | Scheduled drift job |

## Notes

- All `sp-*` names and the `123456789012` account ID are placeholders — replace with your own.
- The plan artifact can contain sensitive values; the workflow keeps `retention-days: 5` and splits read (`GitHubTerraformPlan`) vs write (`GitHubTerraformApply`) roles.
- `drift-check.sh` exits 1 on drift so a scheduled CI job turns red — remediation stays a human decision.
