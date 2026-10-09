# Git Branching Strategies — Companion Resources

Companion files for [Git Branching Strategies Compared](https://stackpractices.com/guides/git-branching-strategies-guide/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `branch-protection-rules.json` | GitHub API payload: required checks, reviews, linear history, no force pushes for `main` and `develop` |
| `github-flow-ci.yml` | GitHub Actions CI gate — tests + lint required before merge to `main` (GitHub Flow / trunk-based) |

## How to use

1. Apply protection rules: `PUT /repos/{owner}/{repo}/branches/{branch}/protection` with the JSON payload (or recreate them in repo Settings → Branches).
2. Copy `github-flow-ci.yml` to `.github/workflows/` and adapt job names to your stack.

The strategy only works if the gates are enforced — protection rules and required checks are the enforcement layer.