variable "region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "production"
}

variable "cidr_block" {
  type    = string
  default = "10.0.0.0/16"
}

variable "availability_zones" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

# One NAT gateway per AZ for prod (no single point of failure, no cross-AZ
# transfer cost). Set to true for cost-sensitive dev environments.
variable "single_nat_gateway" {
  type    = bool
  default = false
}
