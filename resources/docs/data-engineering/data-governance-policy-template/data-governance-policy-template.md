# Data Governance Policy — `<Organization Name>`

## Policy Overview

| Field | Value |
|-------|-------|
| Organization | Example Corp |
| Policy Version | 2.0 |
| Last Updated | 2026-07-05 |
| Policy Owner | Chief Data Officer |
| Approved By | Executive Committee |
| Review Cycle | Annual |
| Next Review | 2027-07-05 |
| Compliance Frameworks | GDPR, CCPA, SOC 2, HIPAA |
| Data Steward | Data Governance Team |

## 1. Data Classification

### Classification Levels

| Level | Name | Description | Examples | Handling Requirements |
|-------|------|-------------|----------|----------------------|
| L1 | Public | No restriction on access | Marketing materials, public docs | No special handling |
| L2 | Internal | Internal use only, no external sharing | Internal reports, project docs | Access control, no external sharing |
| L3 | Confidential | Restricted access, need-to-know | Financial data, customer lists | Encryption, access logging, need-to-know |
| L4 | Restricted | Highest sensitivity, strict access | PII, PHI, payment data, credentials | Encryption, MFA, audit logging, DLP |

### Classification Rules

| Data Type | Classification | Rationale |
|-----------|---------------|-----------|
| Customer names + emails | L4 (Restricted) | PII under GDPR/CCPA |
| Customer addresses | L4 (Restricted) | PII under GDPR/CCPA |
| Payment card numbers | L4 (Restricted) | PCI-DSS requirements |
| Employee salaries | L3 (Confidential) | Internal financial data |
| Product catalog | L2 (Internal) | Competitive advantage |
| Marketing materials | L1 (Public) | Intended for public release |
| Aggregate sales metrics | L2 (Internal) | No individual identification |
| Server IP addresses | L3 (Confidential) | Infrastructure security |
| API keys and secrets | L4 (Restricted) | Credential exposure risk |
| Health records (if applicable) | L4 (Restricted) | PHI under HIPAA |

### Classification Process

| Step | Action | Responsible | Frequency |
|------|--------|-------------|-----------|
| 1 | Identify new data source | Data Engineer | On new source |
| 2 | Classify data fields | Data Steward | On new source |
| 3 | Review classification | Data Governance Team | On new source |
| 4 | Apply classification labels | Data Engineer | After approval |
| 5 | Audit classifications | Data Steward | Quarterly |

## 2. Data Retention

### Retention Schedule

| Data Category | Classification | Retention Period | Disposal Method | Legal Basis |
|---------------|---------------|-----------------|-----------------|-------------|
| Customer PII (active accounts) | L4 | Duration of account + 30 days | Secure deletion | GDPR Article 5(1)(e) |
| Customer PII (closed accounts) | L4 | 30 days after closure | Secure deletion | GDPR right to erasure |
| Transaction records | L3 | 7 years | Secure deletion | Tax regulations |
| Financial reports | L3 | 7 years | Secure deletion | SOX requirements |
| Employee records | L3 | 7 years after termination | Secure deletion | Labor law requirements |
| System logs (security) | L3 | 1 year | Automated purge | SOC 2 requirements |
| System logs (access) | L3 | 90 days | Automated purge | Internal policy |
| Audit trails | L3 | 3 years | Secure deletion | SOC 2 requirements |
| Backups | L2 | 30 days | Overwrite cycle | Operational recovery |
| Marketing data | L2 | 2 years | Secure deletion | Internal policy |
| Aggregated analytics | L2 | 5 years | Secure deletion | Internal policy |
| Data lake raw files | L2 | 90 days | Automated lifecycle | Storage cost management |

### Retention Enforcement

| Mechanism | Data | Implementation | Verification |
|-----------|------|----------------|--------------|
| Automated S3 lifecycle | Data lake raw files | S3 lifecycle policy: transition to Glacier after 30 days, delete after 90 days | Monthly audit: `aws s3api list-objects` count vs. expected |
| Database purge job | System logs | Scheduled SQL job: `DELETE FROM access_logs WHERE created_at < NOW() - INTERVAL '90 days'` | Weekly check: row count of oldest records |
| Secure deletion script | Customer PII | `shred -vfz -n 3` for files, `DROP TABLE` for databases | Quarterly audit: verify no records older than retention period |
| Backup rotation | All backups | Automated backup rotation: daily backups kept 30 days | Monthly check: backup inventory |

## 3. Access Control

### Role-Based Access Control (RBAC)

| Role | Description | Data Access | Platform Access |
|------|-------------|-------------|-----------------|
| Data Consumer | Read aggregated data | L1, L2 (aggregated only) | BI tool (read-only) |
| Data Analyst | Query and analyze data | L1, L2, L3 (assigned datasets) | BI tool, query tool |
| Data Engineer | Build and maintain pipelines | L1, L2, L3, L4 (masked) | Airflow, dbt, S3, Redshift |
| Data Steward | Manage data classification | L1, L2, L3, L4 (assigned domains) | Governance tool, classification system |
| Data Scientist | Build ML models | L1, L2, L3 (assigned datasets) | ML platform, notebooks |
| DBA | Manage databases | L1, L2, L3, L4 (operational) | Database admin tools |
| Compliance Officer | Audit data access | Access logs only | Audit tool, governance dashboard |
| Data Platform Admin | Full platform access | All data (emergency only) | All systems, break-glass |

### Access Request Process

| Step | Action | Approver | SLA |
|------|--------|----------|-----|
| 1 | Submit access request | — | — |
| 2 | Manager approval | Direct manager | 2 business days |
| 3 | Data steward approval | Domain data steward | 3 business days |
| 4 | Provision access | IT/Platform team | 1 business day |
| 5 | Notify requester | — | Same day |
| 6 | Record in access log | Compliance team | 1 business day |

### Access Review Schedule

| Scope | Frequency | Reviewer | Action |
|-------|-----------|----------|--------|
| All data access | Quarterly | Data Steward | Remove unused access |
| L4 (Restricted) access | Monthly | Data Governance Lead | Verify need-to-know |
| Admin/break-glass access | Monthly | CISO | Audit usage |
| Departed employees | Immediate (on departure) | HR + IT | Revoke all access within 24h |

## 4. Privacy and Compliance

### GDPR Compliance

| Requirement | Implementation | Owner | Verification |
|-------------|----------------|-------|--------------|
| Right to access | Data subject request portal, 30-day response SLA | Privacy Team | Quarterly audit of request logs |
| Right to erasure | Automated deletion workflow, 30-day SLA | Data Engineering | Monthly test of deletion procedure |
| Right to portability | JSON export of all user data | Data Engineering | Quarterly test of export |
| Consent management | Consent management platform (CMP) | Product Team | Monthly audit of consent records |
| Data breach notification | 72-hour notification to authorities | Legal + Security | Annual breach response drill |
| Data processing records | Record of Processing Activities (ROPA) | Data Governance | Quarterly ROPA review |
| Data Protection Officer | Appointed DPO | Executive Committee | Annual DPO review |
| Privacy by design | Privacy review in design phase | Product + Legal | Privacy review in every feature PR |

### CCPA Compliance

| Requirement | Implementation | Owner | Verification |
|-------------|----------------|-------|--------------|
| Right to know | Data request portal, 45-day response SLA | Privacy Team | Quarterly audit |
| Right to delete | Same as GDPR erasure | Data Engineering | Monthly test |
| Right to opt-out | "Do Not Sell My Info" page | Product Team | Monthly check of opt-out mechanism |
| Non-discrimination | No service degradation for opt-out | Product Team | Quarterly review |

### Data Processing Records (ROPA)

| Field | Value |
|-------|-------|
| Processing Activity | Customer order processing |
| Data Controller | Example Corp |
| Data Processor | AWS (cloud infrastructure) |
| Purpose | Order fulfillment and analytics |
| Data Categories | Name, email, address, payment info |
| Data Subjects | Customers |
| Retention | 7 years (transaction records) |
| Legal Basis | Contract performance (GDPR Article 6(1)(b)) |
| Transfer Mechanism | SCCs (Standard Contractual Clauses) |
| Security Measures | Encryption at rest, encryption in transit, access control |

## 5. Data Security

### Encryption Requirements

| Classification | At Rest | In Transit | Key Management |
|---------------|---------|-----------|----------------|
| L1 (Public) | Optional | TLS 1.2+ | — |
| L2 (Internal) | AES-256 | TLS 1.2+ | AWS KMS |
| L3 (Confidential) | AES-256 | TLS 1.2+ | AWS KMS with rotation |
| L4 (Restricted) | AES-256 + field-level | TLS 1.3 | AWS KMS + HSM |

### Data Loss Prevention (DLP)

| Channel | DLP Rule | Action | Alert |
|---------|----------|--------|-------|
| Email | Block L3/L4 data in attachments | Block + notify sender | Security team |
| Slack | Detect L4 patterns (SSN, card numbers) | Alert + quarantine message | Security team |
| USB | Block USB writes for L3/L4 | Block + log | Security team |
| Cloud upload | Detect L4 data in uploads to unapproved services | Block + notify user | Security team |
| API responses | Mask L4 fields in non-production environments | Mask (e.g., ****1234) | — |

### Audit Logging

| Event | Log Fields | Retention | Alert |
|-------|-----------|-----------|-------|
| Data access (L3/L4) | User, timestamp, dataset, action, IP | 1 year | Unusual access patterns |
| Data modification (L3/L4) | User, timestamp, dataset, before/after values | 3 years | Unauthorized modifications |
| Access grant/revoke | Admin, target user, role, timestamp | 3 years | Privilege escalation |
| Export/download (L3/L4) | User, dataset, format, record count, timestamp | 1 year | Bulk exports |
| Failed access attempts | User, dataset, timestamp, IP | 90 days | Brute force patterns |

## 6. Data Quality and Lineage

### Data Lineage Requirements

| Requirement | Implementation | Owner |
|-------------|----------------|-------|
| Source-to-sink lineage | dbt model dependencies + Airflow DAG | Data Engineering |
| Column-level lineage | dbt column-level lineage | Data Engineering |
| Transformation documentation | Pipeline design documents | Data Engineering |
| Data freshness tracking | dbt freshness checks | Data Engineering |
| Lineage visualization | Data catalog tool (e.g., Amundsen, DataHub) | Data Platform |

### Data Quality Standards

| Standard | Target | Measurement | Owner |
|----------|--------|-------------|-------|
| Completeness | > 99.5% for required fields | Data quality rules (dbt tests) | Data Steward |
| Accuracy | > 99% for critical metrics | Reconciliation against source | Data Steward |
| Freshness | < 24 hours for production data | dbt freshness checks | Data Engineering |
| Consistency | 100% referential integrity | dbt relationship tests | Data Engineering |
| Uniqueness | 100% for primary keys | dbt unique tests | Data Engineering |

## 7. Incident Response

### Data Breach Response

| Step | Action | Responsible | SLA |
|------|--------|-------------|-----|
| 1 | Detect and confirm breach | Security Team | Immediate |
| 2 | Contain breach (revoke access, isolate systems) | Security + IT | 1 hour |
| 3 | Assess scope and impact | Security + Data Governance | 4 hours |
| 4 | Notify legal team | Security Team | 4 hours |
| 5 | Notify authorities (GDPR: 72 hours) | Legal Team | 72 hours |
| 6 | Notify affected individuals | Legal + Comms | Without undue delay |
| 7 | Document incident | Security Team | 24 hours |
| 8 | Post-incident review | All stakeholders | 2 weeks |
| 9 | Implement corrective actions | Responsible teams | Per action plan |

### Incident Classification

| Severity | Description | Examples | Response |
|----------|-------------|----------|----------|
| Critical | L4 data exposed to unauthorized party | PII leak, payment data breach | Immediate, all steps |
| High | L3 data exposed or L4 access by unauthorized internal user | Financial data leak | Same day, all steps |
| Medium | L2 data exposed or policy violation | Internal docs shared externally | 2 business days |
| Low | Policy violation without data exposure | Missing access log | 5 business days |
