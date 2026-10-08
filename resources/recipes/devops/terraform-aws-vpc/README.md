# Provision an AWS VPC with Terraform

Complete Terraform configuration for a production-ready AWS VPC: public and private subnets across three availability zones, NAT gateways, route tables, least-privilege security groups, VPC Flow Logs, and VPC endpoints.

Companion code for the StackPractices recipe:
[Provision an AWS VPC with Terraform](https://stackpractices.com/recipes/terraform-aws-vpc/)

## Usage

```bash
terraform init
terraform plan -var="region=us-east-1"
terraform apply
```

For a cost-sensitive dev environment with a single NAT gateway:

```bash
terraform apply -var="single_nat_gateway=true"
```

## Files

| File | Contents |
|---|---|
| `versions.tf` | Provider requirements and region |
| `variables.tf` | Region, CIDR, AZs, `single_nat_gateway` toggle |
| `vpc.tf` | VPC, public and private subnets |
| `gateways.tf` | Internet Gateway, EIPs, NAT gateways |
| `routing.tf` | Public/private route tables and associations |
| `security.tf` | Web and database security groups |
| `flow_logs.tf` | VPC Flow Logs to CloudWatch |
| `endpoints.tf` | S3 gateway endpoint, Secrets Manager interface endpoint |
| `nacls.tf` | Network ACL for the public subnets |
| `outputs.tf` | VPC, subnet, and security group IDs |

## Notes

- With `single_nat_gateway=false` (default), one NAT gateway runs per AZ — no single point of failure and no cross-AZ transfer charges.
- Requires AWS credentials configured (`aws configure` or environment variables) and Terraform >= 1.5.
