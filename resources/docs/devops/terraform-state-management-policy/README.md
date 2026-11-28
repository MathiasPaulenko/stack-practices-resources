# Terraform State Management Policy

Companion files for the StackPractices doc template:
<https://stackpractices.com/docs/terraform-state-management-policy/>

## What's here

- `POLICY.md` — ready-to-fill policy document (10 sections: backend, isolation,
  access control, operations, security, DR, CI/CD, migrations, enforcement,
  metrics). Replace the `<...>` placeholders and adopt it.
- `backend.tf` — S3 backend block with native locking (`use_lockfile`,
  Terraform >= 1.10) and DynamoDB migration notes.
- `iam-policies.json` — read-only (plan) and read-write (apply) IAM policies
  for the state bucket, including the `*.tflock` lock permissions.

## Usage

1. Copy `POLICY.md` into your repo/wiki and fill the placeholders.
2. Adapt `backend.tf` to your bucket names and regions.
3. Attach the IAM policies to your user and CI roles.
4. Set the quarterly review date and the first exception register entry.
