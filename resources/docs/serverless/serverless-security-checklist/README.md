# Serverless Security Checklist — Companion Resources

Runnable assets matching the [Serverless Security Checklist](https://stackpractices.com/docs/serverless-security-checklist/).

## Contents

| File | Purpose |
|------|---------|
| `mask-pii.py` | PII masking helper — hashes sensitive fields (email, phone, ssn, creditCard) before they reach logs |
| `security-logger.py` | Structured security-event logger: auth failures, authz failures, JSON output with `security_event` marker for SIEM routing |
| `dependabot.yml` | Weekly dependency update PRs — place at `.github/dependabot.yml` |
| `security-audit.sh` | Dependency audit gate: npm audit, pip safety, Snyk and lockfile provenance check in one pass |

## Usage

```bash
# run the dependency audit in CI or locally
./security-audit.sh

# copy dependabot config into your repo
cp dependabot.yml .github/dependabot.yml
```

`security-logger.py` expects `authenticate`, `authorize` and `process_order` from your own codebase — it's a reference integration, not a drop-in handler. Route the `security_event: true` lines to a dedicated log group or SIEM stream with tighter access than application logs.
