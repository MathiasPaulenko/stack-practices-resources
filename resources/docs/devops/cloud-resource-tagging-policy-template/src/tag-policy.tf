variable "required_tags" {
  type = map(string)
  default = {
    team        = ""
    environment = ""
    product     = ""
    cost-center = ""
    owner       = ""
  }
}

locals {
  default_tags = {
    team        = var.required_tags["team"]
    environment = var.required_tags["environment"]
    product     = var.required_tags["product"]
    cost-center = var.required_tags["cost-center"]
    owner       = var.required_tags["owner"]
    managed-by  = "terraform"
  }
}

resource "aws_instance" "app" {
  ami           = data.aws_ami.app.id
  instance_type = var.instance_type
  tags          = local.default_tags
}

resource "aws_s3_bucket" "data" {
  bucket = var.bucket_name
  tags   = local.default_tags
}

resource "aws_db_instance" "database" {
  engine         = "postgres"
  instance_class = var.db_class
  tags           = local.default_tags
}
