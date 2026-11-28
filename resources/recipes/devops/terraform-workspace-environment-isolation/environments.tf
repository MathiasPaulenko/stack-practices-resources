# Per-workspace configuration via terraform.workspace.
# Valid inside locals/resources/outputs — never inside backend/provider blocks.
locals {
  env_config = {
    dev = {
      instance_type     = "t3.micro"
      min_capacity      = 1
      max_capacity      = 2
      db_instance       = "db.t3.micro"
      enable_monitoring = false
    }
    staging = {
      instance_type     = "t3.small"
      min_capacity      = 2
      max_capacity      = 4
      db_instance       = "db.t3.small"
      enable_monitoring = true
    }
    production = {
      instance_type     = "t3.medium"
      min_capacity      = 3
      max_capacity      = 10
      db_instance       = "db.t3.medium"
      enable_monitoring = true
    }
  }

  config = local.env_config[terraform.workspace]
}

# Example conditional resource: monitoring only where enabled.
# resource "aws_cloudwatch_log_group" "app" {
#   count             = local.config.enable_monitoring ? 1 : 0
#   name              = "/app/${terraform.workspace}"
#   retention_in_days = terraform.workspace == "production" ? 90 : 30
# }
