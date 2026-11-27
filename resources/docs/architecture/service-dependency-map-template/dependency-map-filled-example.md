# Service Dependency Map: `checkout-service`

## 1. Service Metadata

| Field | Value |
|-------|-------|
| Service | `checkout-service` |
| Owner Team | `@team-payments` |
| Repository | `github.com/acme/checkout-service` |
| Runtime | `Kubernetes` |
| Last Updated | `2026-11-26` |

## 2. Upstream Dependencies (This Service Consumes)

| Service | Protocol | Endpoint / Topic | Purpose | Critical? | Fallback |
|---------|----------|------------------|---------|-----------|----------|
| cart-service | HTTP | GET /carts/{id} | Load cart contents | Yes | Reject checkout (cart required) |
| payment-service | gRPC | Charge() | Authorize payment | Yes | Queue payload for replay + page |
| fraud-service | HTTP | POST /score | Fraud scoring | Yes (transitive via payment) | 300ms timeout, proceed without score |
| user-service | HTTP | GET /users/{id} | Identity validation | Yes | Cached JWT for 5 min |
| inventory-service | Event | `inventory.reserve` | Hold stock | No | Reserve post-payment |
| email-service | Event | `email.receipt` | Send receipt | No | DLQ, replay later |

## 3. Downstream Dependencies (Services Consuming This)

| Service | Protocol | Endpoint / Topic | Purpose | Rate Limit |
|---------|----------|------------------|---------|------------|
| web-storefront | HTTP | POST /checkout | Buyer checkout | 2,000/min |
| mobile-app | HTTP | POST /checkout | Buyer checkout | 1,500/min |
| refunds-service | HTTP | POST /checkout/{id}/refund | Refund flow | 200/min |
| analytics-pipeline | Event | `order.completed` | Order events | unlimited |

## 4. External Dependencies

| Vendor | Service | Purpose | SLA | Escalation |
|--------|---------|---------|-----|------------|
| Stripe | Payment API | Card processing | 99.9% | TAM + status.stripe.com |
| SendGrid | Email API | Receipts | 99.9% | status.sendgrid.com |
| MaxMind | Fraud API | IP scoring | 99.5% | support ticket |

## 5. Critical Path Analysis

| Flow | Services Involved | Max Acceptable Latency | Risk if Broken |
|------|-------------------|------------------------|----------------|
| Checkout | web → cart → checkout → payment → ledger | 2s | Revenue loss |
| Refund | refunds → checkout → payment → ledger | 5s | SLA breach with enterprise tenants |
| Order analytics | checkout → kafka → analytics | n/a (async) | Delayed reporting |

## 6. Failure Impact Matrix

| Dependency Fails | Direct Impact | Cascading Impact | Mitigation |
|------------------|---------------|------------------|------------|
| payment-service | Cannot checkout | Revenue stops | Queue replay + immediate page |
| fraud-service | payment latency ×3 | Checkout p99 breach | 300ms timeout + skip score |
| cart-service | Cannot load cart | Checkout blocked | None — hard dependency, alert |
| user-service | Cannot validate identity | All flows stop | Cached JWT + degraded mode |
| email-service | Receipts delayed | Support tickets | DLQ + daily replay |

## 7. Diagram Representation

```
[web-storefront] ──→ [checkout-service] ──→ [cart-service]
                           │
          ┌────────────────┼─────────────────┐
          ↓                ↓                 ↓
   [payment-service]  [fraud-service]   [user-service]
          │                                   │
          ↓                                   ↓
      [Stripe]                          [session-cache]
```

- Notes: fraud-service is reached both directly and transitively via payment-service — document both edges.
- email-service and analytics-pipeline are event-driven: they don't appear in request traces, only in consumer lag metrics.
