# environments.tf — Per-environment state isolation.
# In a real repo each environment is its own root module; this file shows the
# two backend blocks side by side. Keep only one per module.

# environments/dev/backend.tf
# terraform {
#   backend "s3" {
#     bucket       = "my-company-terraform-state"
#     key          = "dev/terraform.tfstate"
#     region       = "us-east-1"
#     use_lockfile = true
#     encrypt      = true
#   }
# }

# environments/production/backend.tf
# terraform {
#   backend "s3" {
#     bucket       = "my-company-terraform-state"
#     key          = "prod/terraform.tfstate"
#     region       = "us-east-1"
#     use_lockfile = true
#     encrypt      = true
#   }
# }

# Workspaces alternative: a single key, the backend namespaces each
# workspace under env:/{workspace}/{key} automatically.
#   terraform workspace new dev
#   terraform workspace new production
#   terraform workspace select production
