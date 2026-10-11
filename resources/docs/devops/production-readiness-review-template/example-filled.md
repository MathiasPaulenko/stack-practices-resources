# PRR: Real-time Notification Service

## Service

- Name: notification-service
- Type: Microservice (Go)
- Tier: 1 (Critical for user experience)
- Review date: 2026-07-11

## Review Findings

| Item | Finding | Risk | Mitigation | Owner | Due |
|------|---------|------|------------|-------|-----|
| Observability | No WebSocket dashboard | Medium | Create dashboard before launch | alice | 2026-07-15 |
| Alerting | No alert for rejected connections | High | Add alert before launch | bob | 2026-07-14 |
| Security | JWT validation missing expiry test | High | Add test before launch | carol | 2026-07-14 |
| Documentation | No rollback runbook | Medium | Write runbook before launch | alice | 2026-07-16 |
| Operational | On-call not trained on WebSocket | Medium | Training session | platform | 2026-07-18 |

## Sign-Off

| Role | Name | Date | Decision |
|------|------|------|----------|
| Engineering owner | alice | 2026-07-18 | Conditional approve |
| Product owner | dave | 2026-07-18 | Approve |
| Security reviewer | carol | 2026-07-18 | Approve (test added) |
| SRE / Platform | bob | 2026-07-18 | Conditional approve |

## Decision

Conditionally approved. Launch permitted after completing the
3 High-risk items (alerting, security, test). Medium-risk items
tracked with due dates but do not block launch.
