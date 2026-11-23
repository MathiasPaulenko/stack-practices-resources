# Pull Request Template

Copy-paste pull request template for GitHub (and adaptable to GitLab, Bitbucket, and Azure DevOps), plus a GitHub Actions workflow that validates required sections and conventional-commit titles.

## Files

- `pull_request_template.md` — the template in English. Save it to `.github/pull_request_template.md` in your repo and GitHub inserts it into every new PR.
- `pull_request_template.es.md` — the same template in Spanish.
- `pr-validation.yml` — GitHub Actions workflow that checks the PR title follows conventional commits and the description keeps the required sections. Save it to `.github/workflows/pr-validation.yml`.

## Usage

```bash
mkdir -p .github
cp pull_request_template.md .github/pull_request_template.md
cp pr-validation.yml .github/workflows/pr-validation.yml
```

For multiple templates, place them in `.github/PULL_REQUEST_TEMPLATE/` (e.g. `feature.md`, `hotfix.md`) and pick one via the `?template=` query parameter.

## Source

- [Pull Request Template — StackPractices](https://stackpractices.com/docs/pull-request-template/)
- [Plantilla de Pull Request — StackPractices](https://stackpractices.com/es/docs/pull-request-template/)
