# Complete Guide to Secrets Management — Companion Scripts

Companion for [Complete Guide to Secrets Management](https://stackpractices.com/guides/complete-guide-secrets-management/).

- `rotate_secret.sh` — zero-downtime rotation: store new version, roll deploy, promote, deprecate old.
- `scan_secrets.sh` — gitleaks history scan for local runs and CI.
- `external-secret.yaml` — External Secrets Operator syncing AWS Secrets Manager into Kubernetes.

Remember: on a scan hit, rotate first — deleting the line does not remove the secret from history.
