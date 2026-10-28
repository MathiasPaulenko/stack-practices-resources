# AWS CLI Bash Scripts

Companion scripts for the [AWS CLI Bash Scripts](https://stackpractices.com/recipes/bash-aws-cli-scripts/) recipe on StackPractices.

Each `.sh` file is self-contained: adjust the variables at the top and run it. All scripts assume AWS CLI v2 is configured (`aws configure`, environment variables, or SSO) and use `set -euo pipefail` so failures stop execution instead of half-applying changes.

## Prerequisites

- AWS CLI v2 (`aws --version`)
- Valid credentials for the target account (IAM user, instance role, or `aws sso login`)
- `jq` — required by `tag-compliance-audit.sh` and `multi-account-deploy.sh`
- GNU `date` — the retention/cutoff snippets use `date -d`; on macOS install coreutils (`brew install coreutils`, then use `gdate`) or adapt to `date -v-30d`

## Scripts

| File | What it does |
| --- | --- |
| `provision-ec2-instance.sh` | Launches an EC2 instance, waits for `running`, prints the public IP |
| `list-ec2-instances.sh` | Table of all instances: ID, state, type, IP, Name tag |
| `ephemeral-vpc.sh` | Creates a tagged VPC + subnet and deletes both on exit (export `KEEP=1` to retain) |
| `s3-bucket-setup.sh` | Creates a bucket (handles the `us-east-1` quirk), enables versioning, applies tiered lifecycle, audits old objects |
| `s3-sync-directory.sh` | Mirrors a local directory to S3 with `--delete` and storage class |
| `stop-ec2-by-tag.sh` | Stops all instances tagged `Environment=dev` (swap for `start-instances` to reverse) |
| `iam-user-audit.sh` | Dumps every IAM user's access keys, attached policies, and groups |
| `rds-snapshot-backup.sh` | Creates an RDS snapshot, waits, prunes snapshots past retention |
| `tag-compliance-audit.sh` | Reports running instances and buckets missing required tags (needs `jq`) |
| `ebs-snapshot-rotation.sh` | Snapshots all `Backup=true` volumes, deletes snapshots older than N days |
| `cleanup-unattached-ebs.sh` | Deletes every unattached (`available`) EBS volume — dry-run first |
| `cost-explorer-report.sh` | Daily spend per service for the last 30 days |
| `cloudwatch-dashboard.sh` | Publishes a CloudWatch dashboard from a JSON body |
| `multi-account-deploy.sh` | Loops dev/staging/prod accounts via `assume-role` and updates a Lambda (needs `jq`) |

## Safety notes

- Scripts that delete or modify resources support a manual dry pass: comment out the delete call or use `--dry-run` where the API supports it (EC2 mutating calls).
- Test against a non-production account first.
- Never embed access keys in scripts — use IAM roles, environment variables, or `aws sts assume-role`.
