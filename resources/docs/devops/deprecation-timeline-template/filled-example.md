# Deprecation Timeline: payments-api v1

> Deprecation owner: payments-platform team | Date: 2027-01-15 | Target shutdown: 2027-10-15
> Replacement: payments-api v2 | Communication channel: #payments-announce + status page

## 1. Deprecation Summary

- **What is being deprecated:** payments-api v1 (`/v1/*` endpoints)
- **Why it is being deprecated:** v2 introduces idempotent payment intents, unified error codes, and PCI-scoped tokenization; v1 maintenance cost exceeds its remaining value
- **What replaces it:** payments-api v2 (`/v2/*`)
- **Who is affected:** 34 known consumer services; 4 enterprise customers with contractual notice clauses
- **Final shutdown date:** 2027-10-15

## 2. Timeline

| Milestone | Date | Description | Owner | Status |
|-----------|------|-------------|-------|--------|
| Announcement | 2027-01-15 | Blog post, changelog, direct email to top 10 consumers | PM | Done |
| Documentation | 2027-02-01 | v1→v2 migration guide published | DevRel | Done |
| Code samples | 2027-02-15 | Migration examples in JS, Python, Java | Payments team | Done |
| Soft warning | 2027-04-01 | `Deprecation` and `Sunset` response headers on all v1 calls | Backend | Done |
| Hard warning | 2027-07-01 | Weekly emails to owners of services still hitting v1 | PM | Scheduled |
| Feature freeze | 2027-07-15 | No new v1 capabilities; critical fixes only | Backend | Scheduled |
| Final cutoff | 2027-10-15 | v1 returns HTTP 410 with migration link | Backend | Scheduled |
| Post-shutdown | 2027-11-15 | Traffic monitoring ends; retrospective | PM | Scheduled |

## 3. Communication Plan

| Audience | Channel | Message | Date |
|----------|---------|---------|------|
| Internal teams | #payments-announce, eng all-hands | v1 deprecation overview + owner asks | 2027-01-15 |
| External developers | Blog post, changelog, newsletter | v2 benefits + migration guide link | 2027-01-15 |
| Enterprise customers | Account manager direct outreach | Contract-compliant notice + dedicated support | 2027-01-10 |
| Support team | Internal briefing doc | Talking points, escalation path | 2027-01-12 |
| Marketing / community | Status page banner | Shutdown date visibility | 2027-07-01 |

## 4. Migration Path

### For consumers using v1 charge endpoints

1. Replace `POST /v1/charges` with `POST /v2/payment-intents`
2. Switch from synchronous capture to `confirm: true` on the intent
3. Map v1 error codes (`card_declined`, `insufficient_funds`) to v2 `failure_reason` enum
4. Update SDK to `payments-client >= 3.0.0` (v2-only)

### Breaking changes

| Old behavior | New behavior | Action required |
|-------------|-------------|-----------------|
| `POST /v1/charges` captures immediately | `POST /v2/payment-intents` creates intent; capture via `confirm` | Update integration flow |
| `amount` in integer cents | `amount` object `{ value, currency }` | Update request builder |
| Webhook `charge.succeeded` | `payment_intent.succeeded` | Update webhook handlers |

## 5. Support Plan

| Support tier | Availability | Contact | Notes |
|-------------|--------------|---------|-------|
| Migration questions | Mon–Fri, office hours Tue/Thu 15:00 UTC | #payments-migration | Recorded sessions available |
| Bug reports on deprecated system | Standard SLA | support@example.com | Critical fixes only after 2027-07-15 |
| Feature requests on deprecated system | Closed | — | Redirected to v2 roadmap |

## 6. Rollback / Grace Period

- [x] Grace period available: Yes
- [x] Grace period duration: 30 days max
- [x] How to request grace period: ticket to payments-platform with migration plan attached
- [x] Criteria for approval: enterprise contract clause OR demonstrated active migration with <2 weeks remaining

## 7. Post-Shutdown

- [x] Monitor for unexpected traffic or errors for 30 days
- [x] Redirect documentation and links to replacement
- [x] Archive deprecation announcement
- [x] Update service catalog to reflect removal
- [x] Hold retrospective with affected consumers
