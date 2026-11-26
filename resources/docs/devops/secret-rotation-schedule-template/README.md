# Secret Rotation Schedule Template — Companion Files

Ready-to-fill files for the [Secret Rotation Schedule Template](https://stackpractices.com/docs/secret-rotation-schedule-template/) on StackPractices.

## Files

| File | What it's for |
|------|---------------|
| `secret-rotation-schedule-template.md` | Full Markdown version of the schedule: inventory, cadence policy, procedures, emergency playbook, escalation, validation checklist, exception log, and metrics table. |
| `secret-inventory.csv` | Spreadsheet-friendly version of the inventory — import it into a secured wiki or governance tool (never a public sheet). |
| `rotation-log.csv` | One row per rotation event: who ran it, what was updated, how it was verified, and the rollback plan. |

## Usage

1. Copy `secret-rotation-schedule-template.md` into your internal wiki and replace every `YYYY-MM-DD` and `@owner` placeholder.
2. Fill the inventory from your secret manager's access logs — not from memory.
3. Use `rotation-log.csv` as the audit trail: append one row after each completed rotation.
4. Store everything behind role-based access control; the schedule itself reveals which secrets exist and when they're vulnerable.
