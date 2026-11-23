# Escalation Policy

## Ladder

| Level | Who | Timeout |
|-------|-----|---------|
| L1 | Primary on-call | Immediate |
| L2 | Secondary on-call | 15 min no-ack or no progress |
| L3 | Service owner team | 15 min after L2 |
| L4 | Incident Commander | SEV-1 declaration |

## Rules

- Escalate early: what's broken, what was tried, what's needed.
- A 5-minute escalation beats a 30-minute solo struggle.
- If a level doesn't ack within the timeout, move up — that's what the ladder is for.
- SEV-1 always gets an Incident Commander; the IC coordinates and does not debug.
