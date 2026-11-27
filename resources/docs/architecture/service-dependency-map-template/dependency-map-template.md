# Service Dependency Map: `<Service Name>`

## 1. Service Metadata

| Field | Value |
|-------|-------|
| Service | `name` |
| Owner Team | `@team-name` |
| Repository | `github.com/org/repo` |
| Runtime | `Kubernetes / ECS / Lambda / VM` |
| Last Updated | `YYYY-MM-DD` |

## 2. Upstream Dependencies (This Service Consumes)

| Service | Protocol | Endpoint / Topic | Purpose | Critical? | Fallback |
|---------|----------|------------------|---------|-----------|----------|
| user-service | HTTP | GET /users/{id} | Auth validation | Yes | Cache for 5 min |
| payment-service | gRPC | Charge() | Process payment | Yes | Queue for retry |
| notification-service | Event | `notify.send` | Send email | No | Skip silently |
| analytics-service | HTTP | POST /events | Track metrics | No | Drop (best effort) |

## 3. Downstream Dependencies (Services Consuming This)

| Service | Protocol | Endpoint / Topic | Purpose | Rate Limit |
|---------|----------|------------------|---------|------------|
| web-frontend | HTTP | GET /api/products | Product catalog | 1,000/min |
| mobile-app | HTTP | GET /api/products | Product catalog | 500/min |
| inventory-service | Event | `inventory.update` | Stock changes | 10,000/hr |

## 4. External Dependencies

| Vendor | Service | Purpose | SLA | Escalation |
|--------|---------|---------|-----|------------|
| Stripe | Payment API | Process cards | 99.9% | support@stripe.com |
| SendGrid | Email API | Transactional email | 99.9% | status.sendgrid.com |
| AWS S3 | Object storage | File uploads | 99.99% | AWS Support |

## 5. Critical Path Analysis

| Flow | Services Involved | Max Acceptable Latency | Risk if Broken |
|------|-------------------|------------------------|----------------|
| Checkout | web → cart → payment → user | 2s | Revenue loss |
| Login | web → user → session-cache | 500ms | User lockout |
| Search | web → search → product-db | 1s | Degraded UX |

## 6. Failure Impact Matrix

| Dependency Fails | Direct Impact | Cascading Impact | Mitigation |
|------------------|---------------|------------------|------------|
| payment-service | Cannot checkout | No revenue | Queue + retry + alert |
| user-service | Cannot authenticate | All flows stop | Cached JWT + degraded mode |
| notification-service | Emails delayed | No cascading | Skip + audit log |

## 7. Diagram Representation

```
[web-frontend] ──→ [product-service] ──→ [product-db]
                        │
                        ↓
              [payment-service] ←── [Stripe]
                        │
                        ↓
           [notification-service] ──→ [SendGrid]
```

- Use C4 diagrams or dependency graphs (Graphviz, Mermaid, Lucidchart)
- Color code: green (healthy), yellow (degraded), red (outage), gray (planned removal)
