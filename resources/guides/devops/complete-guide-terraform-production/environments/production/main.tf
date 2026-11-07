# environments/production/main.tf — thin root module: providers + module
# composition. Resource logic lives in ../../modules (see the sibling
# companion: resources/guides/devops/complete-guide-terraform-modules).
terraform {
  required_version = ">= 1.9"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.80"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "stackpractices" # example — your project name
      Environment = "production"
      ManagedBy   = "terraform"
      Owner       = "platform-team"
    }
  }
}

module "vpc" {
  source = "../../modules/vpc"

  name_prefix        = "sp-prod"
  cidr_block         = "10.10.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  tags = { CostCenter = "platform" }
}

module "eks" {
  source = "../../modules/eks"

  name_prefix     = "sp-prod"
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnet_ids
  cluster_version = "1.33"
  node_groups = {
    general = {
      desired_size   = 3
      min_size       = 2
      max_size       = 6
      instance_types = ["t3.large"]
    }
  }

  tags = { CostCenter = "platform" }
}
