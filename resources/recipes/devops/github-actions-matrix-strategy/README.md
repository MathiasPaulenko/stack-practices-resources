# GitHub Actions Matrix Strategy — Runnable Workflows

Companion files for the StackPractices recipe
[github-actions-matrix-strategy](https://stackpractices.com/recipes/github-actions-matrix-strategy/).

Copy `.github/` into a Node.js repository and push — the workflows spawn real matrix jobs you can watch in the Actions tab.

## Files

| File | What it demonstrates |
|---|---|
| `.github/workflows/matrix-static.yml` | 3×3 OS × Node matrix with `exclude`, `include` (extra coverage cell), `fail-fast: false`, per-cell job names and cache keys |
| `.github/workflows/matrix-services.yml` | Service-container matrix: PostgreSQL and MySQL via `include`-carried config |
| `.github/workflows/matrix-dynamic.yml` | `prepare` job emits the axis from `supported-versions.json`; empty-array guard so a broken file fails loudly |
| `.github/supported-versions.json` | Single source of truth for the dynamic axis — edit it and the matrix follows |

## Usage

```bash
# Copy into any Node.js repo
cp -r .github /path/to/your/repo/

# Then push — the three workflows appear in the Actions tab
```

The workflows expect `npm ci` + `npm test` to work. Swap in your own commands if your repo uses another stack — the matrix mechanics are language-agnostic.
