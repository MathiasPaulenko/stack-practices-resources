run "vpc_plan" {
  command = plan

  variables {
    name            = "test-vpc"
    cidr_block      = "10.99.0.0/16"
    azs             = ["us-east-1a", "us-east-1b"]
    public_subnets  = ["10.99.1.0/24", "10.99.2.0/24"]
    private_subnets = ["10.99.101.0/24"]
  }

  assert {
    condition     = aws_vpc.this.cidr_block == "10.99.0.0/16"
    error_message = "VPC CIDR did not match the input."
  }

  assert {
    condition     = length(aws_subnet.public) == 2
    error_message = "Expected 2 public subnets."
  }

  assert {
    condition     = length(aws_subnet.private) == 1
    error_message = "Expected 1 private subnet."
  }
}

run "rejects_bad_cidr" {
  command = plan

  variables {
    name       = "test-vpc"
    cidr_block = "not-a-cidr"
  }

  expect_failures = [
    var.cidr_block,
  ]
}
