# Core Web Vitals Audit Checklist — Companion Files

Downloadable artifacts for the [Core Web Vitals Audit Checklist](https://stackpractices.com/docs/core-web-vitals-audit-checklist/) on StackPractices.

## Files

| File | What it is |
|---|---|
| `cwv-issue-tracker.csv` | Issue tracker with example rows — import into Sheets/Jira and replace with your findings |
| `audit-report-template.md` | Blank audit report (field + lab + findings + remediation plan) ready to fill |
| `web-vitals-rum.js` | RUM collection snippet using the `web-vitals` library — sends LCP/INP/CLS to your endpoint |

## Usage

1. Run the checklist on your page types (tools: Lighthouse, PSI, CrUX, WebPageTest).
2. Log findings in `cwv-issue-tracker.csv` with owner and target.
3. Fill `audit-report-template.md` per audited page.
4. Drop `web-vitals-rum.js` into your app entry point to start collecting field data.

Targets at P75 mobile: **LCP ≤ 2.5s · INP ≤ 200ms · CLS ≤ 0.1**

## Related

- Doc: https://stackpractices.com/docs/core-web-vitals-audit-checklist/
- Web Vitals reference: https://web.dev/vitals/
