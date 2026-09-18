# Frontend Performance Budget Template Resources

Companion resources for [Frontend Performance Budget Template](https://stackpractices.com/docs/frontend-performance-budget-template/).

## Files

| File | Description |
|------|-------------|
| `budget/performance-budget-template.md` | Complete budget document: per-route resource budgets, Core Web Vitals targets, timing budgets, third-party budgets, and RUM/synthetic monitoring thresholds |
| `ci/budget-check.yml` | GitHub Actions workflow running the bundle check and Lighthouse CI on every pull request |
| `ci/check-bundle-size.js` | Node script comparing gzipped asset sizes against budgets; exits non-zero on any overrun (requires `gzip-size`) |
| `ci/lighthouserc.json` | Lighthouse CI config collecting 3 runs on key routes and asserting Core Web Vitals thresholds |

## Usage

1. Copy `budget/performance-budget-template.md` into your repo and fill in your own numbers (measure first — see the article's "How to Set Your Numbers" section).
2. Copy `ci/check-bundle-size.js` to `scripts/` and adjust the file paths and budgets to your build output.
3. Copy `ci/budget-check.yml` to `.github/workflows/` and `ci/lighthouserc.json` to your repo root.
4. Add `gzip-size` and `@lhci/cli` as dev dependencies if not already present.
