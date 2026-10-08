# Data Classification: <System / Dataset>

## 1. Classification Definitions

| Level | Description | Examples | Handling Requirements |
|-------|-------------|----------|----------------------|
| **Public** | Approved for public disclosure | Marketing site, OSS repos, job posts | No access control; standard backups |
| **Internal** | Employees and contractors only | Wikis, roadmaps, non-sensitive metrics | Role-based access; encrypted at rest; MFA remote |
| **Confidential** | Disclosure harms the company | Customer PII, financials, source code | Encrypt rest+transit; least privilege; audit log |
| **Restricted** | Disclosure causes severe harm | Cards, SSNs, health records, keys | Encrypt rest+transit; need-to-know; strict audit |

## 2. Dataset Inventory

| Dataset | Classification | Storage | Encryption | Access Control | Retention | Owner |
|---------|---------------|---------|------------|----------------|-----------|-------|
| `<dataset_name>` | `<level>` | `<storage>` | `<cipher>` | `<who can read/write>` | `<window>` | `@<owner>` |
| | | | | | | |

## 3. Handling Rules by Level

### Access

| Level | Authentication | Authorization | MFA | Remote Access |
|-------|---------------|---------------|-----|---------------|
| Public | None | None | N/A | Open |
| Internal | SSO | Role-based | Required | VPN + MFA |
| Confidential | SSO | Role + approval | Required | VPN + MFA + justification |
| Restricted | SSO + hardware key | Need-to-know + multi-party | Required | Dedicated VPN + justification |

### Transmission

| Level | Internal Network | External Network | Email / Chat |
|-------|-----------------|------------------|--------------|
| Public | Plain | Plain | Allowed |
| Internal | TLS 1.2+ | TLS 1.2+ | Allowed with care |
| Confidential | TLS 1.2+ | TLS 1.2+ + DLP scan | Approved channels only |
| Restricted | TLS 1.2+ + mTLS | Prohibited — secure transfer | Prohibited — approved exchange |

### Storage

| Level | Encryption at Rest | Key Management | Backup | Geolocation |
|-------|-------------------|----------------|--------|-------------|
| Public | Optional | Standard | Standard | Any region |
| Internal | AES-256 | Standard | AES-256 | Approved regions |
| Confidential | AES-256 | HSM or KMS | AES-256 | Approved regions + residency |
| Restricted | AES-256-GCM | HSM | AES-256 + air-gapped | Approved regions, no cross-border |

## 4. Exception Log

| Dataset | Requested Lower Level | Justification | Risk Accepted By | Date | Review Date |
|---------|----------------------|---------------|------------------|------|-------------|
| | | | | | |

End of document. Review and update quarterly.
