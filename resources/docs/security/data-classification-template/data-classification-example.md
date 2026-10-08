# Data Classification: Acme Analytics (worked example)

> Completed example of the classification template for a small B2B SaaS.
> Shows how to reason about each dataset, not just fill in columns.

## 1. Classification Definitions

Uses the standard four levels from the template: Public, Internal,
Confidential, Restricted.

## 2. Dataset Inventory

| Dataset | Classification | Storage | Encryption | Access Control | Retention | Owner |
|---------|---------------|---------|------------|----------------|-----------|-------|
| `customers.user_profiles` | Confidential | PostgreSQL RDS | AES-256 | RBAC: eng, support | 7y post-deletion | @data-team |
| `billing.payment_tokens` | Restricted | Vault / HSM | AES-256-GCM | Payments team only | 90 days | @payments-lead |
| `analytics.events` | Internal | ClickHouse warehouse | AES-256 | Employees | 24 months | @analytics-lead |
| `logs.app_requests` | Confidential | S3 (private) | AES-256 | Eng + SRE | 30 days | @sre-lead |
| `db_backups.nightly` | Restricted | S3 (isolated account) | AES-256 + KMS | Backup role only | 35 days | @infra-lead |
| `blog.content` | Public | S3 (public) | None | None | Indefinite | @marketing |
| `sales.pipeline_export` | Confidential | CRM export, shared drive | AES-256 | Sales leadership | 12 months | @sales-ops |

## 3. Decisions Worth Documenting

- `logs.app_requests` was bumped from Internal to Confidential because the
  request logs carry user IDs and paths — PII by any reasonable reading.
- `db_backups.nightly` inherited the highest level present in the dump
  (Restricted) and moved out of the shared backup bucket into an isolated
  account with a dedicated KMS key.
- `analytics.events` stays Internal only while the documented PII filter
  runs in the pipeline. That filter is tracked as an exception log entry
  with a quarterly review — if the filter is ever bypassed, the dataset
  reclassifies to Confidential.

## 4. Exception Log

| Dataset | Requested Lower Level | Justification | Risk Accepted By | Date | Review Date |
|---------|----------------------|---------------|------------------|------|-------------|
| `analytics.events` | Internal (vs Confidential) | PII filter strips identifiers pre-ingest | @cto | 2026-01-15 | 2026-04-15 |
| `sales.pipeline_export` | Internal sharing (vs Confidential) | Board reporting cycle needs wide visibility | @cro | 2026-02-01 | 2026-05-01 |

End of document. Review and update quarterly.
