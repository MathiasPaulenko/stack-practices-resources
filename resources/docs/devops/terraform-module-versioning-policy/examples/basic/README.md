# Basic Usage Example

Minimal consumer of the module with an exact version pin — the recommended
default for production per the pinning table in the policy.

```hcl
module "my_module" {
  source  = "myorg/my-module/aws"
  version = "2.3.1"

  name        = "my-app"
  environment = "production"
}
```

Run:

```bash
terraform init
terraform plan
```
