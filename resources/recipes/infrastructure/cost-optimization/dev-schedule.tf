# dev-schedule.tf — Scheduled scaling for non-production environments.
# Dev/staging runs 9:00–18:00 UTC Mon–Fri: 45 of 168 weekly hours (~73% saved).
#
# Attach to an existing Auto Scaling group:
#   terraform apply -var="asg_name=my-dev-asg"

variable "asg_name" {
  description = "Auto Scaling group to schedule (dev or staging)"
  type        = string
}

variable "timezone" {
  description = "IANA timezone for the schedule"
  type        = string
  default     = "UTC"
}

resource "aws_autoscaling_schedule" "dev_scale_up" {
  scheduled_action_name  = "dev-office-hours-up"
  min_size               = 1
  max_size               = 3
  desired_capacity       = 2
  recurrence             = "0 9 * * MON-FRI"
  time_zone              = var.timezone
  autoscaling_group_name = var.asg_name
}

resource "aws_autoscaling_schedule" "dev_scale_down" {
  scheduled_action_name  = "dev-off-hours-down"
  min_size               = 0
  max_size               = 0
  desired_capacity       = 0
  recurrence             = "0 18 * * MON-FRI"
  time_zone              = var.timezone
  autoscaling_group_name = var.asg_name
}

# Optional: also shut down for the whole weekend is implied by MON-FRI above.
# For standalone EC2/RDS instances outside an ASG, pair this with
# aws_instance_scheduler (the AWS Instance Scheduler solution) or EventBridge
# Scheduler + Lambda calling stop_instances / start_instances by tag
# (e.g. Schedule=office-hours).
