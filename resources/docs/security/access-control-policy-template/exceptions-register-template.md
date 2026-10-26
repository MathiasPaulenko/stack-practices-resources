# Access Control Exceptions Register — `<Organization Name>`

Every deviation from the access control policy gets a row here. Exceptions without an expiry date are violations waiting to be discovered — review this register at each policy review.

| ID | Exception | Justification | Approved By | Approved On | Expires On | Status |
|----|-----------|---------------|-------------|-------------|------------|--------|
| EX-001 | Legacy billing system cannot enforce MFA | Vendor limitation; compensating control is IP allowlist | CISO | 2026-01-15 | 2026-07-15 | Active |
| EX-002 | Monitoring service account has standing prod read | Alerting dependency; scoped to read-only | Manager + CISO | 2026-02-01 | 2026-08-01 | Active |
| EX-003 | | | | | | |

## Rules

- No exception without an expiry date and a named owner.
- Expired exceptions are either formally renewed (new expiry, new approval) or fixed.
- Review the register quarterly alongside the privileged-access review.
