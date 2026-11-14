variable "cidr" {
  type        = string
  description = "CIDR block for the VPC (e.g. \"10.0.0.0/16\")."
}

variable "name" {
  type        = string
  description = "Environment name used in resource names and tags."
}

variable "region" {
  type        = string
  description = "AWS region; subnet AZs are derived from it (a, b, c)."
}
