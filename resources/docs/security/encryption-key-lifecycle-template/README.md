# Encryption Key Lifecycle Template

Companion files for the [Encryption Key Lifecycle Template](https://stackpractices.com/docs/encryption-key-lifecycle-template/) on StackPractices.

## Contents

| File | Purpose |
|------|---------|
| `kms-key-policy.yaml` | CloudFormation snippet for an AWS KMS key with automatic rotation and a least-privilege key policy |
| `key-rotation-audit.sh` | Bash script that lists all KMS keys in a region and flags the ones without automatic rotation |
| `key-compromise-runbook.md` | Step-by-step response runbook for a key compromise incident |

## Usage

1. Adapt `kms-key-policy.yaml` to your account: replace `app-role` with the IAM role your application uses and review which admin actions each principal needs.
2. Run the audit script against your region to find keys missing rotation:

   ```bash
   chmod +x key-rotation-audit.sh
   ./key-rotation-audit.sh
   ```

   Requires the AWS CLI configured with `kms:ListKeys`, `kms:DescribeKey` and `kms:GetKeyRotationStatus` permissions. Change `REGION` at the top of the script as needed.
3. Keep `key-compromise-runbook.md` accessible from your incident tooling and rehearse it in a tabletop exercise before you need it.

The lifecycle policy tables (classification, rotation, access control, inventory, metrics, compliance mapping) live in the template itself — copy them into your internal docs and fill in your own values.
