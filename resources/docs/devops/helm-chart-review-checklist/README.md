# Helm Chart Review Checklist — Companion Files

Standalone files for the [Helm Chart Review Checklist](https://stackpractices.com/docs/helm-chart-review-checklist/) doc on StackPractices.

## Contents

| File | What it is |
|------|-----------|
| `src/helm-chart-review-checklist.md` | The complete fillable checklist — copy it into your repo (e.g. `.github/helm-review.md`) and fill the Status column per chart |
| `src/chart-review-ci.yml` | GitHub Actions workflow that automates the checklist: `helm lint`, `helm template`, `kube-score`, `:latest` tag and plaintext-secret detection, dry-run upgrade |

## Usage

```bash
# Drop the checklist into a PR when reviewing a chart manually
cp src/helm-chart-review-checklist.md .github/helm-review.md

# Or automate the review gate in CI
cp src/chart-review-ci.yml .github/workflows/helm-chart-review.yml
```

Adjust `./charts/my-app` to your chart path. The workflow fails the PR on `:latest` tags, plaintext secrets in `values.yaml`, or kube-score warnings — the same checks the manual checklist covers.
