# security-review-checklist-for-prs

Companion resources for the [Security Review Checklist for PRs](https://stackpractices.com/docs/security-review-checklist-for-prs/) guide on StackPractices.com.

## Files

| File | Purpose |
|------|---------|
| `pre-commit-config.yaml` | Pre-commit hooks for GitLeaks and detect-secrets |
| `semgrep.yml` | Custom Semgrep security rules for PR review |
| `security-review.yml` | GitHub Actions workflow for automated security checks |

## Usage

1. Copy `pre-commit-config.yaml` to your repo root and run `pre-commit install`.
2. Copy `semgrep.yml` to your repo root and run `semgrep --config semgrep.yml`.
3. Copy `security-review.yml` to `.github/workflows/` and set the `SNYK_TOKEN` secret.

## Requirements

- [pre-commit](https://pre-commit.com/) >= 3.0
- [Semgrep](https://semgrep.dev/) >= 1.0
- [Snyk CLI](https://snyk.io/) (optional, for dependency scanning)
- [GitLeaks](https://github.com/gitleaks/gitleaks) >= 8.0
