# Microservice Contract: `<Consumer>` ↔ `<Provider>`

## 1. Parties

| Role | Service | Team | Contact |
|------|---------|------|---------|
| Provider | `service-name` | `@team` | `email / slack` |
| Consumer | `consumer-name` | `@team` | `email / slack` |

## 2. API Specification

- **Protocol**: REST / gRPC / GraphQL / Message Queue
- **Base URL / Topic**: `https://api.internal/...` or `kafka://events/...`
- **OpenAPI / Schema Link**: `link-to-spec`
- **Authentication**: mTLS / JWT / API Key / None

## 3. Endpoints / Operations

| Name | Method / Operation | Path / Topic | Purpose |
|------|-------------------|--------------|---------|
| GetUser | GET | `/users/{id}` | Retrieve user profile |
| CreateOrder | POST | `/orders` | Submit a new order |
| OrderCreated | Event | `orders.created` | Notify downstream systems |

## 4. Service Level Agreement

| Metric | Target | Measurement |
|--------|--------|-------------|
| Availability | 99.9% | Monthly uptime |
| p95 Latency | < 200ms | Per endpoint |
| Error Rate | < 0.1% | 5xx / timeout ratio |
| RPO | 1 hour | Max acceptable data loss |
| RTO | 30 minutes | Max recovery time |

## 5. Versioning Policy

- **Current Version**: `v2`
- **Strategy**: URL path (`/v1/`, `/v2/`) / Header / Content negotiation
- **Deprecation Window**: 6 months after new version release
- **Sunset Notice**: 30 days before removal

## 6. Breaking Changes

A change is breaking if it:
- Removes a field or endpoint
- Changes field type or format
- Tightens validation rules
- Changes error response structure

**Procedure**:
1. Notify consumers 30 days in advance
2. Release new version alongside old version
3. Monitor old version usage
4. Remove old version after deprecation window

## 7. Error Handling

| Error Code | HTTP / gRPC | Meaning | Retryable |
|------------|-------------|---------|-----------|
| 400 / INVALID_ARGUMENT | Client error | No |
| 429 / RESOURCE_EXHAUSTED | Rate limited | Yes (with backoff) |
| 500 / INTERNAL | Server error | Yes (with backoff) |

## 8. Escalation

- **P1 (outage)**: Page on-call within 15 minutes
- **P2 (degraded)**: Slack channel alert, respond within 1 hour
- **P3 (question)**: Open a ticket, respond within 1 business day
