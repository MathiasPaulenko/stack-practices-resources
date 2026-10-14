# Bug Report Template — Companion Resources

Companion files for the [Bug Report Template](https://stackpractices.com/docs/bug-report-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `bug-report-template.md` | Markdown | Copy-paste ready bug report template with severity levels and evidence fields |
| `github-issue-form.yml` | YAML | GitHub issue form that enforces reproduction steps and severity as required fields |
| `gitlab-issue-template.md` | Markdown | GitLab issue description template — drop into `.gitlab/issue_templates/` |

## Quick start

### 1. Copy the Markdown template

```bash
cp bug-report-template.md BUG-1234-export-empty-file.md
```

Edit the copy and replace every placeholder (`'...'`, `[e.g., ...]`) with real values.

### 2. Install the GitHub issue form

```bash
mkdir -p .github/ISSUE_TEMPLATE
cp github-issue-form.yml .github/ISSUE_TEMPLATE/bug-report.yml
```

Commit and push — reporters will now see a structured form instead of a blank textarea, and `validations.required` blocks submission without reproduction steps.

### 3. GitLab alternative

```bash
mkdir -p .gitlab/issue_templates
cp gitlab-issue-template.md .gitlab/issue_templates/Bug.md
```

GitLab prefills the description from the template when someone picks it in the new-issue form. Field enforcement is by convention — the template includes the same sections plus `/label ~bug ~triage` quick actions at the bottom.

## Template structure

1. **Summary** — what breaks, where, under what condition
2. **Steps to Reproduce** — numbered, from a known state
3. **Expected vs Actual Behavior** — defines what "fixed" means
4. **Environment** — OS, browser, app version, deployment environment
5. **Introduced In** — first version where the bug appears
6. **Severity** — Critical / High / Medium / Low
7. **Evidence** — screenshots, logs, request IDs
8. **Additional Context** — frequency, related work, recent changes
