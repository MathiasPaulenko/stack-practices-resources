# SOC 2 Compliance Guide — Companion

Evidence artifacts for the controls from the guide:

- `soc2-evidence-map.md` — control → evidence → automation mapping for the nine Common Criteria families.
- `access_review_diff.py` — compares two quarterly IAM exports (CSV) and reports additions, removals, and role changes. The diff plus the review ticket is your CC6 evidence.
- `pr_approval_export.py` — exports reviewers on merged PRs through the GitHub REST API into a CSV audit trail for CC8.
- `vendor-due-diligence-checklist.md` — repeatable vendor onboarding/review checklist for CC9 and subservice-organization tracking.

## Usage

1. Point `access_review_diff.py` at this quarter's and last quarter's IAM exports: `python access_review_diff.py q1.csv q2.csv`.
2. Set `GITHUB_TOKEN` and run `pr_approval_export.py` monthly to archive the approval trail.
3. Keep one completed `vendor-due-diligence-checklist.md` per subservice organization, reviewed annually.

Source article: <https://stackpractices.com/guides/compliance-soc2-guide/>
