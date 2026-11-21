# Microservice Contract: `checkout-web` ↔ `payments-service`

## 1. Parties

| Role | Service | Team | Contact |
|------|---------|------|---------|
| Provider | `payments-service` | `@payments` | `#team-payments` |
| Consumer | `checkout-web` | `@checkout` | `#team-checkout` |

## 2. API Specification

- **Protocol**: REST over HTTPS
- **Base URL**: `https://api.internal/payments/v2`
- **OpenAPI**: `https://specs.internal/payments/v2/openapi.yaml`
- **Authentication**: mTLS via service mesh

## 3. Endpoints / Operations

| Name | Method | Path | Purpose |
|------|--------|------|---------|
| CreateCharge | POST | `/charges` | Authorize and capture a payment |
| GetCharge | GET | `/charges/{id}` | Retrieve charge status |
| RefundCharge | POST | `/charges/{id}/refunds` | Full or partial refund |
| ChargeRefunded | Event | `payments.refunded` | Async refund confirmation |

## 4. Service Level Agreement

| Metric | Target | Measurement |
|--------|--------|-------------|
| Availability | 99.95% | Monthly, excl. planned maintenance |
| p95 Latency | < 300ms | Per endpoint, 5-min windows |
| Error Rate | < 0.5% | 5xx + timeouts / total requests |

## 5. Versioning Policy

- **Current**: `v2` (v1 deprecated, sunset 2027-03-01)
- **Strategy**: URL path versioning
- **Deprecation Window**: 6 months after successor release

## 6. Breaking Changes

Field removals, type changes, and new required fields are breaking.
Provider opens a deprecation notice, keeps both versions live for the
window, and tracks v1 traffic weekly until it reaches zero.

## 7. Escalation

- **P1**: Page `#payments-oncall` — 15 min response
- **P2**: `#team-payments` Slack — 1 hour
- **P3**: Ticket — next business day
