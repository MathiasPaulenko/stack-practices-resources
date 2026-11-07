# Technical Debt Management — Runnable Companion

Companion code for the guide [Technical Debt: Track, Prioritize, Pay Down](https://stackpractices.com/guides/complete-guide-technical-debt-management/).

## Files

- `debt-prioritizer.js` — scores debt items by impact, interest and effort, then ranks them. Ships with the sample register from the guide so you can see why the payment-test item outranks the bigger auth refactor.
- `measure-debt.js` — a monthly debt snapshot: TODO/FIXME counts and outdated dependencies are computed directly; coverage and duplication are read from `coverage/coverage-summary.json` and `report/jscpd-report.json` when you already run those tools.
- `templates/debt-register.md` — the register format with a filled example.
- `templates/stakeholder-report.md` — the top-five report skeleton for asking management for paydown capacity.

## Run

```bash
node debt-prioritizer.js
node measure-debt.js            # scans the current directory
node measure-debt.js ../my-app  # or point it at a source tree
```

Expected output of the prioritizer: TD-002 first (critical impact beats higher effort), TD-003 last (low impact, high effort — the "ignore" quadrant).
