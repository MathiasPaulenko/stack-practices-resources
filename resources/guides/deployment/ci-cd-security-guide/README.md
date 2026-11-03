# CI/CD Security Guide Resources

Companion resources for [CI/CD Pipeline Security: Prevent Supply Chain Attacks](https://stackpractices.com/guides/ci-cd-security-guide/).

## Files

| File | Description |
|------|-------------|
| `ci/secure-workflow.yml` | Hardened GitHub Actions workflow: SHA-pinned actions, minimal permissions, OIDC auth, Trivy scan, cosign signing, manual production approval |
| `ci/runner-hardening-checklist.md` | Checklist for self-hosted runner security: isolation, rootless builds, ephemeral runners, audit logging |

## Usage

1. Copy `ci/secure-workflow.yml` to `.github/workflows/` and adjust the role ARN, region, and image name.
2. Work through `ci/runner-hardening-checklist.md` for any self-hosted runners.
