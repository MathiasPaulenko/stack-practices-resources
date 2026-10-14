# versions.tf — Terraform and provider version constraints
# Pin a floor for Terraform and a compatible range for each provider.
# Raising the floor is a breaking change — bump MAJOR when you edit this.

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 6.0"
    }
  }
}
