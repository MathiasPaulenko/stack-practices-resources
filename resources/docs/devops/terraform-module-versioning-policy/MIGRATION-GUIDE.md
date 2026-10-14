# Migration Guide: v1.x to v2.x

## Breaking Changes

1. `instance_type` variable removed → use `instance_types` (list)
2. `tags` output changed from `map(string)` to `map(any)`
3. Minimum Terraform version raised from 1.0 to 1.5

## Migration Steps

1. Update the module version in your configuration:

   ```hcl
   module "my_module" {
     source  = "myorg/my-module/aws"
     version = "2.0.0"
   }
   ```

2. Replace `instance_type` with `instance_types`:

   ```hcl
   # Before (v1.x)
   module "my_module" {
     instance_type = "t3.micro"
   }

   # After (v2.x)
   module "my_module" {
     instance_types = ["t3.micro"]
   }
   ```

3. Run `terraform init -upgrade` to download the new version.
4. Run `terraform plan` and review the changes.
5. Run `terraform apply` when ready.
