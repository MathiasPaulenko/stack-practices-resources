# Complete Guide to AWS Cost Optimization — Companion Files

Scripts and configs referenced by the guide:
[Complete Guide to AWS Cost Optimization](https://stackpractices.com/guides/complete-guide-cost-optimization-aws/)

## Contents

| File | What it does |
|------|--------------|
| `budget-alert.sh` | Creates a monthly AWS budget with an 80% actual-spend email alert. |
| `s3-lifecycle-policy.json` | Lifecycle rule: STANDARD → IA (30d) → GLACIER (90d) → DEEP_ARCHIVE (365d), plus a 7-day expiry for temp objects. |
| `ec2-fleet-spot.json` | EC2 Fleet request for Spot capacity using the `capacity-optimized` allocation strategy across 3 instance types. |
| `spot-asg-vpc-endpoints.tf` | Terraform: mixed on-demand/Spot ASG plus a free S3 gateway endpoint and a DynamoDB interface endpoint. |
| `spot-interruption-check.py` | Polls IMDSv2 for the two-minute Spot termination notice and calls a graceful shutdown hook. |
| `rds-snapshot-cleanup.py` | Deletes manual RDS snapshots older than 30 days, paginated, skipping in-use snapshots. |
| `cost-report-lambda.py` | Lambda handler that reports services above $100/month to Slack; schedule with EventBridge. |

## Usage

- Shell/Python scripts expect AWS CLI v2 credentials with billing, EC2, RDS and CloudWatch permissions.
- `ec2-fleet-spot.json` is meant for `aws ec2 create-fleet --cli-input-json file://ec2-fleet-spot.json` — replace the launch template ID and subnets with your own.
- `spot-asg-vpc-endpoints.tf` references `aws_launch_template.app`, `aws_vpc.main`, `aws_route_table.private` and `aws_subnet.private` — wire them to your VPC module.
- Prices mentioned in the guide are illustrative us-east-1 figures; check AWS Pricing for current rates.
