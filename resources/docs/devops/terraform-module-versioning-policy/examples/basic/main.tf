# examples/basic/main.tf — consuming the module with an exact version pin
# Production default: pin the exact version, upgrade deliberately.

module "my_module" {
  source  = "myorg/my-module/aws"
  version = "2.3.1"

  name        = "my-app"
  environment = "production"
}
