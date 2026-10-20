# Secrets Rotation Template — Companion Resources

Downloadable files for the [Secrets Rotation Template](https://stackpractices.com/docs/secrets-rotation-template/) article.

## Files

| File | Purpose |
|------|---------|
| `secrets-rotation-schedule.md` | Blank rotation schedule with cadence policy, emergency playbook, exception log and metrics tables |
| `rotation-runbook-db.sh` | Zero-downtime database rotation script using the dual-read pattern |
| `rotation-validation-checklist.md` | Per-rotation checklist: transition, pre-revocation and post-revocation |
| `rotation-log-example.md` | Filled rotation log for a production database credential |

## How to use

1. Copy `secrets-rotation-schedule.md` and fill the inventory from your secret manager's access logs.
2. Assign cadences and owners per secret type; set 30/14/7-day alerts.
3. Pilot the procedure with `rotation-runbook-db.sh` on a low-risk secret.
4. Attach a completed `rotation-validation-checklist.md` to every rotation log.

Spanish version: [Plantilla de Rotación de Secretos](https://stackpractices.com/es/docs/secrets-rotation-template/)
