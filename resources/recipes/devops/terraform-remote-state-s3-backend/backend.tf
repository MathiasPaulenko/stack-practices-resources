# backend.tf — S3 backend with native locking (Terraform >= 1.10).
# Copy into each root module; change `key` per environment/component.

terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket       = "my-company-terraform-state"
    key          = "infrastructure/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true # Native locking, no DynamoDB table needed
    encrypt      = true
  }
}

# Migrating from a DynamoDB-locked setup:
#   1. Remove `dynamodb_table`, set `use_lockfile = true`
#   2. Run `terraform init -reconfigure`
#   3. Keep the table until every workspace has migrated, then delete it
