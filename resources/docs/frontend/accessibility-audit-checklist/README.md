# Accessibility Audit Checklist — Companion Resources

Companion files for the [Accessibility Audit Checklist](https://stackpractices.com/docs/accessibility-audit-checklist/) on StackPractices.

## Contents

| File | Purpose |
|------|---------|
| `accessibility-audit-checklist-template.md` | Blank WCAG 2.2 audit: audit info, testing tools, all 86 criteria tables, failed-criteria summary, remediation plan — ready to fill in |
| `axe-playwright.spec.ts` | Playwright + axe-core spec that runs WCAG 2.1/2.2 AA automated checks on every scoped page in CI |
| `.pa11yci.json` | pa11y-ci config for a second automated pass (WCAG2AA) — catches a different slice of issues than axe |

## Usage

```bash
# Automated pass with Playwright + axe
npm i -D @playwright/test @axe-core/playwright
npx playwright test axe-playwright.spec.ts

# Or with pa11y-ci against a running preview
npm i -D pa11y-ci
npx pa11y-ci --config .pa11yci.json
```

Fill the template's audit-information table first, record every automated-scan result as a row, then do the manual keyboard pass and the screen-reader pass — the checklist's test-method column exists to keep those honest.
