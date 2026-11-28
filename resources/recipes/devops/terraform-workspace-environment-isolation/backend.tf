# Remote state on S3 with native lockfile locking (Terraform >= 1.10).
# One key serves every workspace: the S3 backend stores each workspace's
# state under env:/<workspace>/ inside the bucket automatically.
# Do NOT interpolate terraform.workspace here — backends are evaluated
# before workspace selection, so it fails at terraform init.
terraform {
  required_version = ">= 1.10.0"

  backend "s3" {
    bucket       = "my-company-terraform-state"
    key          = "infrastructure/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
    # Optional: use a custom prefix instead of the default "env:"
    # workspace_key_prefix = "workspaces"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
