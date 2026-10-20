# Terraform module with mandatory tags
# Every resource gets the baseline tags unless the module overrides them.

variable "required_tags" {
  type = map(string)
  default = {
    Team        = "platform"
    Environment = "production"
    Project     = "api-gateway"
    CostCenter  = "PL-0001"
  }
}

resource "aws_instance" "app" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.medium"
  tags          = var.required_tags
}

# Tag validation in CI — fail the plan if a tag is missing
resource "null_resource" "tag_validator" {
  provisioner "local-exec" {
    command = "python3 scripts/validate_tags.py --tfplan tfplan.json"
  }
}
