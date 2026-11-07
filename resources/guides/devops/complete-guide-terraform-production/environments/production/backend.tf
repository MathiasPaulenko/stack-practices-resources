# environments/production/backend.tf
# Native S3 state locking (Terraform >= 1.10). No DynamoDB table needed —
# dynamodb_table is deprecated; use_lockfile replaces it.
terraform {
  backend "s3" {
    bucket       = "sp-terraform-state-prod" # example — must match bootstrap output
    key          = "production/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
    # encrypt defaults to true (SSE-S3). For SSE-KMS: kms_key_id = "arn:aws:kms:..."
    # Recommended for auditability:
    # assume_role = { role_arn = "arn:aws:iam::123456789012:role/TerraformStateAccess" }
  }
}
