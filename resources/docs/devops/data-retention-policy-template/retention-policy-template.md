# [Organization] Data Retention Policy

- Policy name: `[Policy name]`
- Effective date: `YYYY-MM-DD`
- Review cycle: `[Annually / Quarterly]`
- Policy owner: `[Team]`
- Legal approver: `[Name / Role]`
- Technical owner: `[Team]`
- Scope: `[Systems and data covered]`

## 1. Data Categories and Retention Periods

| Data Category | Examples | Retention Period | Archive After | Delete After | Legal Basis |
|---------------|----------|------------------|---------------|--------------|-------------|
| Customer account data | Profiles, preferences | Life of account + [N] | [N] after close | [N] after close | Contract |
| Transaction records | Orders, payments | [N] years | [N] | [N] after period close | Tax law |
| Application logs | Request, error logs | [N] days | [N] days | [N] days | Operational need |
| Security logs | Auth, access logs | [N] | [N] | [N] | Compliance |
| Backups | Full / incremental | [N] days | [N] days | Per backup schedule | DR |
| Analytics data | Aggregated events | [N] | [N] | [N] | Legitimate interest |
| Marketing data | Emails, leads | [N] or until opt-out | [N] | On opt-out or [N] | Consent |
| Temporary data | Cache, imports | [N] days | [N] days | [N] days | Operational need |

## 2. Retention Rules by Classification

| Classification | Minimum Retention | Maximum Retention | Special Handling |
|----------------|-------------------|-------------------|------------------|
| Public | As needed | [N] | None |
| Internal | Business need | [N] | Standard lifecycle |
| Confidential | Legal/contract minimum | [N] | Encryption, access logs |
| Restricted | Regulatory minimum | Regulatory maximum | Legal hold, encryption, audit trail |

## 3. Deletion and Verification Checklist

- [ ] Data owner confirms retention period has expired.
- [ ] No active legal hold covers the data.
- [ ] Data deleted from primary storage and indexes.
- [ ] Backups purged or scheduled for purge within policy.
- [ ] Archives deleted or anonymized per schedule.
- [ ] Derived datasets, caches, and replicas refreshed or cleared.
- [ ] Deletion logged with timestamp, owner, and scope.
- [ ] Sample verified to confirm deletion.
- [ ] Compliance team reviews deletion logs periodically.

> See `s3-lifecycle.json` for automated lifecycle transitions and `purge.sql` for scheduled database purges.
