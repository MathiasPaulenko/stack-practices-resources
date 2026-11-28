# Terraform State Management Policy — <Organization Name>

> Companion template for https://stackpractices.com/docs/terraform-state-management-policy/
> Fill in the `<...>` placeholders, adapt the tables to your org, and review quarterly.

## Policy Overview

| Field | Value |
|-------|-------|
| Organization | <Example Corp> |
| Policy Version | 1.1 |
| Last Updated | <YYYY-MM-DD> |
| Policy Owner | <DevOps Team> |
| Approved By | <Head of Infrastructure> |
| Review Cycle | Quarterly |
| Terraform Version | 1.10+ |
| Backend | S3 with native locking (AWS) |
| State Encryption | AES-256 (S3 server-side) |

## 1. Backend Configuration

### Required Backend: S3 with Native Locking

| Component | Purpose | Configuration |
|-----------|---------|---------------|
| S3 bucket | State file storage | Encrypted, versioned, private |
| `.tflock` object | State locking | Native `use_lockfile`, no DynamoDB |
| KMS key | Encryption key | Customer-managed, rotated annually |
| IAM policy | Access control | Least privilege per environment |

### Backend Naming Convention

| Environment | S3 Bucket | State Key |
|-------------|-----------|---------------|
| Production | <org>-tfstate-prod | `<project>/terraform.tfstate` |
| Staging | <org>-tfstate-staging | `<project>/terraform.tfstate` |
| Development | <org>-tfstate-dev | `<project>/terraform.tfstate` |
| Shared | <org>-tfstate-shared | `<project>/terraform.tfstate` |

## 2. State Isolation

| Level | Isolation Method | Rationale |
|-------|-----------------|-----------|
| Environment | Separate S3 buckets | Prod and dev never share state |
| Project | Separate state keys | Projects don't depend on each other |
| Team | Separate AWS accounts | Full isolation for compliance |
| Region | Separate state per region | Regional infrastructure isolation |

## 3. Access Control

See `iam-policies.json` for ready-to-adapt read-only (plan) and read-write
(apply) IAM policies. Key rule: users get read access; only the CI service
account and senior DevOps get write access on production state.

## 4. State Operations

Prohibited: local state, manual state editing, `apply` without plan,
`force-unlock` without investigation, state sharing across environments.

## 5. State Security

Encrypt at rest, block all public access, mark sensitive variables, and keep
secrets in a dedicated store (Vault, AWS Secrets Manager) — not in Terraform.

## 6. Disaster Recovery

Primary recovery: S3 versioning (`aws s3api copy-object` a previous version).
Secondary: weekly manual export, 90-day retention. Lockfiles need no backup —
they are transient.

## 7. CI/CD Integration

Plan on every PR, apply on merge to main, no manual applies. Use a service
account with an IAM role — never user credentials.

## 8. Legacy Migrations

DynamoDB locking (pre-1.10): remove `dynamodb_table`, set `use_lockfile = true`,
run `terraform init -reconfigure` per workspace, delete the table when done.

## 9. Enforcement and Exceptions

Every exception needs an owner and an expiry date recorded in this document.
Expired exceptions are violations.

## 10. Metrics and Review

Track: % of applies via CI/CD, stale locks per month, state files without
versioning, public state objects, expired exceptions. Review quarterly.
