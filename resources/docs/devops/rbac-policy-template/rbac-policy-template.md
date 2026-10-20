# RBAC Policy — [Organization / System Name]

> Fill in the bracketed placeholders. Store this document next to the IAM code it describes.

## 1. Purpose and Scope

This policy governs access to **[system names, environments, and data classifications]**. It applies to all employees, contractors, and service accounts. Access is granted through named roles only; direct permission grants outside this policy require a documented exception approved by **[risk committee / security team]**.

## 2. Policy Statement

All access to systems, data, and infrastructure is granted based on predefined roles. Roles align with job functions, least privilege, and separation of duties. Every assignment requires documented approval, is logged in the access register, and is reviewed on the cadence defined in section 7.

## 3. Role Definitions

| Role | Description | Permissions | Scope | Approval Required |
|------|-------------|-------------|-------|-------------------|
| viewer | Read-only access for reporting and investigation | read | All resources | Manager |
| editor | Modify configuration and non-production data | read, write | Non-production | Manager |
| operator | Deploy, restart, and monitor services | read, deploy, restart | Assigned services | Team lead |
| admin | Full access for break-glass and critical changes | full | Entire system | Security + manager |
| auditor | Read-only access to logs and compliance evidence | read | Logs and audit data | Compliance officer |

<!-- Add or remove roles here. Aim for three to seven roles per system. -->

## 4. Role Assignment Rules

| Rule | Description |
|------|-------------|
| Least privilege | Users receive the minimum role needed for their current duties. |
| Separation of duties | No single user holds roles that let them both make and approve sensitive changes. |
| Time-bound | Temporary or elevated roles expire automatically. |
| Manager approval | Role assignment requires documented approval from the user's manager. |
| Revocation on change | Roles are revoked when a user changes teams or leaves the organization. |
| One privileged identity | Admin duties run on a separate privileged account, never on the daily-use account. |

## 5. Separation of Duties Matrix

| Role A | Role B | Conflict | Resolution |
|--------|--------|----------|------------|
| editor | approver | Can write and approve own changes | Split duties or require peer approval |
| operator | auditor | Can act and erase the audit trail | Assign audit to a different team |
| admin | any other role | Superset — other roles are redundant | Hold only admin, time-bound |
| requester | approver (self) | Self-approval defeats the control | Approver must be a different person |

<!-- Extend with combinations specific to your systems. -->

## 6. Access Request Workflow

| Step | Action | Owner | SLA |
|------|--------|-------|-----|
| 1 | User submits request with business justification | Requester | N/A |
| 2 | Manager reviews and approves | Manager | 2 business days |
| 3 | Role is provisioned by identity or platform team | IAM team | 1 business day |
| 4 | Assignment is logged in access register | IAM team | Same day |
| 5 | Access is reviewed during quarterly audit | System owner | Quarterly |

Emergency requests bypass the SLA, not the control: an incident commander can approve a time-bound `operator` grant verbally, but it must be logged within 24 hours and expire automatically.

## 7. Review and Compliance

| Activity | Frequency | Owner | Evidence |
|----------|-----------|-------|----------|
| Role inventory review | Annually | Security | Updated role matrix |
| Privileged access review | Quarterly | System owner | Attestation record |
| Orphan account cleanup | Quarterly | IAM team | Disabled account list |
| Exception approval | As needed | Risk committee | Risk acceptance form |

## 8. Offboarding and Role Changes

When someone changes teams or leaves, their roles are revoked the same day the HR system marks the transition. Deprovisioning is automated through the identity provider's group sync.

## 9. Break-Glass Access

Emergency access uses dedicated break-glass accounts with sealed credentials. Every use triggers an alert and a mandatory post-incident review within 24 hours.

## 10. Exceptions

Exceptions require a written record: requester, compensating control, approver, and expiry date. An exception without an expiry date is a permanent grant.

---

**Document owner:** [name/team] · **Last review:** [date] · **Next review:** [date]
