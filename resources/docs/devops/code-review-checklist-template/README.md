# Code Review Checklist Template — Companion Files

Companion to the StackPractices template [Code Review Checklist Template](https://stackpractices.com/docs/code-review-checklist-template/).

| File | Contains |
|---|---|
| src/code-review-checklist.md | Copy-paste markdown checklist: 7 dimensions, review notes table, verdict, and reviewer confirmation |
| src/code-review-automation.yml | GitHub Actions workflow: CodeQL analysis, lint/typecheck gate, and oversized-PR warning |
| src/pr-checklist-validator.py | Python bot that checks tests added, no secrets in the diff, and a complete PR description |
| src/review-metrics.py | Review metrics script: cycle time, comments per PR, defect escape rate, per-reviewer stats |

## Usage

- Drop `code-review-checklist.md` into your wiki or into `.github/pull_request_template.md`.
- Copy `code-review-automation.yml` to `.github/workflows/` and adjust the CodeQL `languages` list to your stack.
- Run `python src/pr-checklist-validator.py` inside a PR branch (expects `origin/main` as the base).
- Feed `review-metrics.py` with your PR metadata to compute team-level review health.
