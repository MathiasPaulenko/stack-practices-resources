# AWS Basics Guide — Companion Resources

Runnable assets for the [AWS Basics guide](https://stackpractices.com/guides/aws-basics-guide/) on StackPractices.

## Files

| File | Description |
|------|-------------|
| `aws-commands.sh` | AWS CLI commands from the guide: EC2 launch, S3 bucket ops, EBS volume, RDS instance, billing alarm |
| `lambda_handler.py` | Minimal Python Lambda handler |
| `dynamodb_basics.py` | DynamoDB put/get with boto3 |
| `iam-policy.json` | Least-privilege S3 policy example with region condition |

## Usage

1. Set up the AWS CLI and credentials first (`aws configure`).
2. Review every command before running — replace placeholder IDs (`ami-*`, `sg-*`, `subnet-*`, account IDs) with your own.
3. The billing alarm command belongs in `us-east-1` — that's where AWS publishes billing metrics.
