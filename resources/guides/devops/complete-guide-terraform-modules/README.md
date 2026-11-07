# Terraform Modules — VPC Module, Tests & Composition Examples

Companion code for [Complete Guide to Terraform Modules](https://stackpractices.com/guides/complete-guide-terraform-modules/) on StackPractices.

## Layout

```text
modules/vpc/                  # The canonical module from the guide
├── main.tf                   # VPC, subnets (for_each), IGW, NAT, route tables
├── variables.tf              # Inputs with validation blocks
├── outputs.tf                # IDs consumers reference
├── versions.tf               # required_version + provider pins
├── examples/basic/main.tf    # Runnable usage (terraform init && plan)
└── tests/vpc.tftest.hcl      # Native terraform test suite
test/vpc_test.go              # Terratest e2e (real apply, costs money)
```

## Try it

```bash
cd modules/vpc/examples/basic
terraform init
terraform plan          # renders the full resource graph, no apply needed
```

Run the contract tests from the module root:

```bash
cd modules/vpc
terraform init
terraform test          # runs tests/vpc.tftest.hcl
```

The Terratest suite deploys real AWS resources (EIP + NAT gateway have a cost):

```bash
cd test
go test -v -timeout 30m
```

## Notes

- `for_each = toset(var.public_subnets)` keys subnets by CIDR, so removing an entry mid-list does not recreate the rest.
- The private route table sends `0.0.0.0/0` through the NAT gateway — without it, private subnets are created but isolated.
- `azs` can be left empty to use region defaults in a fuller version; here the example passes them explicitly.
