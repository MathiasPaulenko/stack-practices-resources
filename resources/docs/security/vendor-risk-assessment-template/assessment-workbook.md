# Vendor Risk Assessment: `<Vendor Name>`

## 1. Vendor Metadata

| Field | Value |
|-------|-------|
| Vendor Name | `name` |
| Service Provided | `description` |
| Data Access Level | `None / Read / Write / Admin` |
| Data Types Handled | `PII / PHI / Financial / Confidential / Public` |
| Contract Value | `$X / year` |
| Criticality Rating | `Low / Medium / High / Critical` |
| Assessment Date | `YYYY-MM-DD` |
| Assessor | `@security-team` |
| Next Review Date | `YYYY-MM-DD` |

## 2. Security Controls

| Control Category | Vendor Claim | Evidence Requested | Verified | Risk |
|------------------|--------------|-------------------|----------|------|
| SOC 2 Type II | Yes / No | Report (last 12 months) | | |
| ISO 27001:2022 | Yes / No | Certificate | | |
| GDPR / CCPA Compliance | Yes / No | DPA + privacy policy | | |
| Encryption at Rest | Yes / No | Architecture doc / screenshot | | |
| Encryption in Transit (TLS 1.2+) | Yes / No | SSL Labs scan | | |
| MFA for Admin Access | Yes / No | Configuration screenshot | | |
| Penetration Test (annual) | Yes / No | Report summary (redacted) | | |
| Incident Response Plan | Yes / No | Document + SLAs | | |
| Sub-processors Published | Yes / No | Sub-processor list | | |

## 3. Operational Risk

| Factor | Rating | Justification | Mitigation |
|--------|--------|---------------|------------|
| Financial stability | `Low / Med / High` | | |
| Geographic / political risk | `Low / Med / High` | | |
| Concentration risk (sole provider) | `Low / Med / High` | | |
| Integration complexity | `Low / Med / High` | | |
| Exit difficulty (data portability) | `Low / Med / High` | | |

## 4. Data Handling Assessment

| Question | Vendor Response | Satisfactory |
|----------|----------------|--------------|
| Where is data stored? | `Region / country` | Yes / No |
| Who can access our data? | `Role / process` | Yes / No |
| Is data commingled with other customers? | `Yes / No / Multi-tenant` | Yes / No |
| Data retention after contract end? | `Days / policy` | Yes / No |
| Can we request deletion? | `Process / SLA` | Yes / No |
| Backup frequency and retention? | `Frequency / retention` | Yes / No |
| Breach notification within 72h? | `Yes / No` | Yes / No |

## 5. Risk Score

| Category | Weight | Raw Score (1-5) | Weighted Score |
|----------|--------|-----------------|----------------|
| Security posture | 30% | | |
| Compliance | 25% | | |
| Operational resilience | 20% | | |
| Data protection | 25% | | |
| **Total** | **100%** | | |

### Score Interpretation

| Range | Rating | Action |
|-------|--------|--------|
| 4.0 – 5.0 | Low Risk | Standard contract; annual review |
| 3.0 – 3.9 | Medium Risk | Require remediation plan; 6-month review |
| 2.0 – 2.9 | High Risk | Security improvements required before onboarding |
| 1.0 – 1.9 | Critical Risk | Do not onboard without CISO approval + external audit |

## 6. Remediation Plan (if applicable)

| Gap | Required Action | Owner | Due Date | Status |
|-----|----------------|-------|----------|--------|
| | | | | |
