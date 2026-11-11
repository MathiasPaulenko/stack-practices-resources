# Mandatory tagging module for cost allocation.
# Usage:
#   module "tags" {
#     source      = "./tagging_policy"
#     team_email  = "platform@example.com"
#     environment = "production"
#     project     = "billing"
#     cost_center = "CC-1234"
#   }
#   resource "aws_instance" "api" { tags = module.tags.mandatory_tags ... }

variable "team_email" {
  description = "Owning team contact — who pays the bill"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  validation {
    condition     = contains(["production", "staging", "development"], var.environment)
    error_message = "environment must be production, staging, or development."
  }
}

variable "project" {
  description = "Project or product code"
  type        = string
}

variable "cost_center" {
  description = "Finance cost-center tracking code"
  type        = string
}

variable "managed_by" {
  description = "Provisioning tool"
  type        = string
  default     = "terraform"
}

locals {
  mandatory_tags = {
    Owner       = var.team_email
    Environment = var.environment
    Project     = var.project
    CostCenter  = var.cost_center
    ManagedBy   = var.managed_by
  }
}

output "mandatory_tags" {
  value = local.mandatory_tags
}
