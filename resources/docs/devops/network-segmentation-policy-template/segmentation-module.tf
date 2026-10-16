# modules/segmentation/main.tf

variable "vpc_id" {
  type        = string
  description = "VPC where the segment security group is created"
}

variable "environment" {
  type        = string
  description = "Environment name (prod, staging, dev)"
}

variable "allowed_ingress" {
  type = list(object({
    source_cidr = string
    port        = number
    description = string
  }))
  default = []
}

variable "allowed_egress" {
  type = list(object({
    destination_cidr = string
    port             = number
    description      = string
  }))
  default = [
    { destination_cidr = "0.0.0.0/0", port = 443, description = "Outbound HTTPS" }
  ]
}

# AWS security groups deny everything by default — rules only add allows.
resource "aws_security_group" "segment" {
  name        = "${var.environment}-segment-sg"
  description = "Security group for ${var.environment} network segment"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.allowed_ingress
    content {
      description = ingress.value.description
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = [ingress.value.source_cidr]
    }
  }

  dynamic "egress" {
    for_each = var.allowed_egress
    content {
      description = egress.value.description
      from_port   = egress.value.port
      to_port     = egress.value.port
      protocol    = "tcp"
      cidr_blocks = [egress.value.destination_cidr]
    }
  }

  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
    Policy      = "segmentation"
  }
}
