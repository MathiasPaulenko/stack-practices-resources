provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source = "../../"

  name            = "example-vpc"
  cidr_block      = "10.10.0.0/16"
  azs             = ["us-east-1a", "us-east-1b"]
  public_subnets  = ["10.10.1.0/24", "10.10.2.0/24"]
  private_subnets = ["10.10.101.0/24", "10.10.102.0/24"]

  tags = {
    Environment = "example"
    Team        = "platform"
  }
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnet_ids" {
  value = module.vpc.public_subnet_ids
}
