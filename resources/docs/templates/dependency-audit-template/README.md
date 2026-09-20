# Third-Party Dependency Audit Template — Companion Code

Companion resources for [Third-Party Dependency Audit Template](https://stackpractices.com/docs/dependency-audit-template/)
(ES: [Plantilla de Auditoría de Dependencias de Terceros](https://stackpractices.com/es/docs/dependency-audit-template/)).

## What's inside

| File | Description |
|------|-------------|
| `templates/dependency-audit-template.md` | The copy-paste audit record: overview fields, security checks, maintenance health thresholds, supply chain risk, and the three-way decision row |
| `automation/dependabot.yml` | Dependabot config with weekly scans and patch/minor grouping so PRs stay manageable |
| `scripts/license-check.sh` | Scans the production dependency tree and exits non-zero if a copyleft license (GPL/AGPL/LGPL/SSPL/…) hides in a transitive dep |

## Usage

1. Copy `templates/dependency-audit-template.md` into `docs/audits/<library>.md` and fill one per dependency under review.
2. Pull real numbers from [osv.dev](https://osv.dev), [deps.dev](https://deps.dev), and [OpenSSF Scorecard](https://scorecard.dev) — don't fill thresholds from memory.
3. Drop `automation/dependabot.yml` at `.github/dependabot.yml` so new CVEs open PRs automatically.
4. Run `scripts/license-check.sh` in CI on the production tree; a transitive GPL dep should fail the build, not surface in due diligence.
5. Follow the pre-adoption → monitoring → quarterly review → deprecation lifecycle on the main page.

## License

MIT — see the repository root.
