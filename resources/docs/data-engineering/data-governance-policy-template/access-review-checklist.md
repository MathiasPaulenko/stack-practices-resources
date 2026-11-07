# Quarterly Access Review Checklist

Use this checklist every quarter (and monthly for L4 data) to verify that data access matches the RBAC table in the governance policy. Print it, run it, file the result — auditors ask for evidence, not intentions.

## Preparation

- [ ] Export current access grants per dataset (group membership, IAM policies, BI tool permissions)
- [ ] Export last-used timestamp per grant where the platform provides it
- [ ] Pull the list of departures and team changes since the last review
- [ ] Pull open access requests still pending approval

## Review pass

- [ ] Flag every grant unused for 6+ months — revoke unless the owner actively re-justifies it
- [ ] Flag every L4 (Restricted) grant without a documented need-to-know reason
- [ ] Flag shared accounts and service accounts with human owners who left
- [ ] Flag access held by departed employees or contractors — should be zero; investigate any hit
- [ ] Flag access that survives a team change and no longer matches the person's role
- [ ] Verify break-glass / admin accounts: named owner, MFA enabled, usage audited since last review

## Findings and actions

- [ ] Record every revoked grant (user, dataset, reason, date) in the access log
- [ ] Record every exception kept (owner, reason, expiry date)
- [ ] Open tickets for anything that can't be fixed in the review session
- [ ] Update the RBAC table if a role's documented access no longer matches reality

## Sign-off

- [ ] Data steward signs the review summary
- [ ] Compliance officer countersigns for L3/L4 scope
- [ ] File the signed summary where the audit evidence lives
- [ ] Schedule the next review date
