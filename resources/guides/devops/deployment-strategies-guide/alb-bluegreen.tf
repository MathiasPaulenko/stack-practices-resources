# Blue-green deployment behind an AWS Application Load Balancer.
# Cutover = change `live_weight` from blue (100) to green (100) and apply.
# Rollback = flip the weights back — a pure routing change, seconds to revert.

variable "live_target" {
  description = "Which target group serves 100% of traffic: blue or green"
  type        = string
  default     = "blue"
  validation {
    condition     = contains(["blue", "green"], var.live_target)
    error_message = "live_target must be \"blue\" or \"green\"."
  }
}

resource "aws_lb_target_group" "blue" {
  name     = "app-blue"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  health_check {
    path                = "/health"
    interval            = 15
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_lb_target_group" "green" {
  name     = "app-green"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  health_check {
    path                = "/health"
    interval            = 15
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener_rule" "app" {
  listener_arn = var.alb_listener_arn
  priority     = 100

  action {
    type = "forward"
    forward {
      target_group {
        arn    = aws_lb_target_group.blue.arn
        weight = var.live_target == "blue" ? 100 : 0
      }
      target_group {
        arn    = aws_lb_target_group.green.arn
        weight = var.live_target == "green" ? 100 : 0
      }
      stickiness {
        enabled  = false
        duration = 1
      }
    }
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }
}

variable "vpc_id" {
  description = "VPC hosting both target groups"
  type        = string
}

variable "alb_listener_arn" {
  description = "ARN of the ALB listener that owns this rule"
  type        = string
}
