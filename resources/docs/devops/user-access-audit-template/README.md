# User Access Audit Template — Companion Resources

Companion files for the [User Access Audit Template](https://stackpractices.com/docs/user-access-audit-template/) on StackPractices.

## Contents

| File | Purpose |
|------|---------|
| `user-access-audit-template.md` | Blank certification template: scope, inventory, access mapping, privileged review, certification log, remediation plan, evidence checklist |
| `okta-access-review.py` | Pulls active users from the Okta API, flags accounts inactive beyond a threshold, and exports a per-user access CSV |
| `aws-access-analyzer.sh` | Creates (idempotently) an organization-level IAM Access Analyzer and exports active findings to JSON |
| `github-org-audit.js` | Lists GitHub org members, flags users without 2FA (via the `2fa_disabled` filter) and organization admins |

## Usage

```bash
# Okta report
pip install requests
export OKTA_API_TOKEN=ssws_xxx
export OKTA_DOMAIN=yourorg.okta.com
python okta-access-review.py --days 90 --output access_review.csv

# AWS findings export
./aws-access-analyzer.sh us-east-1

# GitHub org audit
npm install @octokit/rest
GITHUB_TOKEN=ghp_xxx node github-org-audit.js your-org
```

## Notes

- The Okta script reads `lastLogin` from the Okta Users API; accounts that never logged in are excluded from the inactivity report and should be reviewed separately.
- `2fa_disabled` filtering requires the token to have admin access to the organization.
- Run privileged access reviews quarterly and general reviews annually, plus on role changes and offboarding.

## Related

- [RBAC Policy Template](https://stackpractices.com/docs/rbac-policy-template/)
- [Access Control Review Template](https://stackpractices.com/docs/access-control-review-template/)
