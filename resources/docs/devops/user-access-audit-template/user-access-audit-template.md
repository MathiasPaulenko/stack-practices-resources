# User Access Audit — [Period]

## 1. Audit Scope

| Scope Item | Description |
|------------|-------------|
| Period | [YYYY-QN] |
| Systems reviewed | [List: AWS, GitHub, Jira, ...] |
| Population | [Employees, contractors, service accounts, privileged roles] |
| Reviewers | [Application owners, managers, security team] |
| Due date | [YYYY-MM-DD] |
| Exceptions allowed | [Yes, with risk acceptance and expiration] |

## 2. Identity Inventory

| User ID | Name | Type | Department | Status | Last Reviewed |
|---------|------|------|------------|--------|---------------|
| `user@example.com` | [Name] | [Employee/Contractor/Service] | [Dept] | [Active/Inactive] | [YYYY-MM-DD] |

## 3. Access Mapping

| User | System | Role / Permission | Business Justification | Reviewer | Decision |
|------|--------|-------------------|--------------------------|----------|----------|
| `user@example.com` | [System] | [Role] | [Why they need it] | [Reviewer] | [Keep/Revoke/Downgrade] |

## 4. Privileged Access Review

| User | System | Privileged Role | Justification | Risk | Reviewer | Decision |
|------|--------|-----------------|---------------|------|----------|----------|
| `user@example.com` | [System] | [Admin/Root/Owner] | [Justification] | [High/Med/Low] | [Reviewer] | [Decision] |

## 5. Certification Log

| Application | Reviewer | Status | Date | Notes |
|-------------|----------|--------|------|-------|
| [App] | [Reviewer] | [Certified/In progress] | [YYYY-MM-DD] | [Notes] |

## 6. Remediation Plan

| Finding | Action | Owner | Due Date | Status |
|---------|--------|-------|----------|--------|
| [Finding] | [Action] | [Owner] | [YYYY-MM-DD] | [Open/In progress/Done] |

## Evidence Bundle (archive after close)

- [ ] Exported identity inventory (per system)
- [ ] Signed certification log
- [ ] Closed remediation tickets / proof of revocation
- [ ] Exceptions with risk acceptance and expiry dates
