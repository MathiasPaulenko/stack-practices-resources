variable "aws_region" {
  description = "AWS region for this environment"
  type        = string
  default     = "us-east-1"
}

# Secrets arrive via TF_VAR_* environment variables in CI — never in tfvars.
variable "db_password" {
  description = "RDS master password (sourced from TF_VAR_db_password in CI)"
  type        = string
  sensitive   = true
}
