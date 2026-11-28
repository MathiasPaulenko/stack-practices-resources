# backend.tf — S3 backend with native locking (Terraform >= 1.10)
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
    bucket       = "example-tfstate-prod"
    key          = "infrastructure/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true # Native locking — no DynamoDB table needed
    kms_key_id   = "alias/terraform-state-key"
  }
}

# Migrating from dynamodb_table (pre-1.10):
#   1. Remove `dynamodb_table`, set `use_lockfile = true`
#   2. Run `terraform init -reconfigure` per workspace
#   3. Keep the table until every workspace migrated, then delete it
