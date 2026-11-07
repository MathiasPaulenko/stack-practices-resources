# Technical Debt Register

Triage: weekly, 10 minutes inside sprint planning.
Close an item only with a merged PR or a shipped deploy.

## TD-XXX: <title>
- **Type**: deliberate / inadvertent / bit rot / dependency / test / documentation / infrastructure
- **Date added**: YYYY-MM-DD
- **Impact**: critical | high | medium | low — what it costs now
- **Interest**: what it costs per sprint/month if left unpaid
- **Effort**: days to fix
- **Owner**: who decides it gets paid
- **Status**: open | scheduled | accepted — and when
- **Resolution**: what "paid" looks like

<!-- Example filled entry:

## TD-002: No integration tests for payment flow
- **Type**: Test debt
- **Date added**: 2026-02-01
- **Impact**: Critical — payment bugs reached production twice this quarter
- **Interest**: ~4 hours of manual regression testing per release
- **Effort**: 3 days
- **Owner**: QA lead
- **Status**: Open — triage Friday
- **Resolution**: Playwright integration tests for the payment flow
-->
