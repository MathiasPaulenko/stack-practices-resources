# budget-alerts.tf — AWS Budgets with email alerts at 80% and 100%.
# Catches cost drift before the invoice arrives.
#
# terraform init && terraform apply -var="alert_email=finops@example.com"

variable "alert_email" {
  description = "Email that receives budget alerts"
  type        = string
}

variable "monthly_limit_usd" {
  description = "Total monthly budget in USD"
  type        = string
  default     = "2000"
}

resource "aws_budgets_budget" "monthly_total" {
  name         = "monthly-total"
  budget_type  = "COST"
  limit_amount = var.monthly_limit_usd
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }

  # Forecasted spend crossing the limit mid-month — earlier than ACTUAL
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.alert_email]
  }
}

# Per-service budget example: alert when EC2 alone exceeds $800
resource "aws_budgets_budget" "ec2_only" {
  name         = "ec2-monthly"
  budget_type  = "COST"
  limit_amount = "800"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filter {
    name   = "Service"
    values = ["Amazon Elastic Compute Cloud - Compute"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 90
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }
}
