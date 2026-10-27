# API Rate Limiting Policy

## Tiers & Limits

| Tier | Requests / Minute | Requests / Hour | Burst | Cost |
|------|-------------------|-------------------|-------|------|
| Free | 60 | 1,000 | 10 | $0 |
| Starter | 300 | 10,000 | 50 | $49/mo |
| Pro | 1,000 | 100,000 | 200 | $199/mo |
| Enterprise | 10,000 | 1,000,000 | 2,000 | Custom |

## Limit Scope

Limits are applied per **API key** at the following scopes:
- **Global:** All endpoints combined count toward the same limit
- **Endpoint-specific:** `POST /orders` has its own limit separate from `GET /products`
- **IP-based (Free tier only):** Fallback enforcement when API key is absent

## Quota Periods

- **Per-minute limit:** Resets at the top of each minute (UTC)
- **Per-hour limit:** Resets at the top of each hour (UTC)
- **Rolling window:** A 60-second sliding window (more precise but computationally expensive)

## Response Headers

Every API response includes the following headers:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1719398400
X-RateLimit-Policy: pro;w=3600
```

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests allowed in the current window |
| `X-RateLimit-Remaining` | Requests remaining in the current window |
| `X-RateLimit-Reset` | Unix timestamp when the current window resets |
| `X-RateLimit-Policy` | Tier and window size identifier |

## Exceeded Limit Response

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "You've exceeded your rate limit. Please retry after 2026-06-26T11:00:00Z.",
    "retryAfter": 3600,
    "documentationUrl": "https://docs.example.com/rate-limits"
  }
}
```

HTTP Status: `429 Too Many Requests`
Required Header: `Retry-After: 3600`

## Burst Behavior

Burst limits allow short spikes above the sustained rate:
- **Pro tier:** 200 requests in 1 second, then throttled to 1,000/hour average
- **Algorithm:** Token bucket with refill rate = sustained limit / window size
- **Penalty:** No penalty for burst usage within configured limits

## Increasing Limits

1. **Upgrade tier:** Change your plan in the developer dashboard
2. **Request exception:** Contact api-support@example.com with:
   - Current usage patterns (requests per endpoint, peak hours)
   - Business justification (product launch, integration partner)
   - Expected timeline and volume
3. **Enterprise negotiation:** Dedicated capacity, custom SLA, private endpoints

## Monitoring & Alerts

| Alert | Condition | Action |
|-------|-----------|--------|
| Approaching Limit | 80% of hourly quota consumed | Email notification to admin |
| Limit Exceeded | 429 responses > 1% of traffic | PagerDuty alert to on-call |
| Abuse Pattern | 10x normal volume from single key | Auto-throttle + manual review |

## Fair Use Policy

- **No automated evasion:** Using several API keys to circumvent limits violates terms
- **Cache aggressively:** Responses marked `Cache-Control: public` should be cached
- **Batch operations:** Use bulk endpoints instead of individual calls
- **Webhook preference:** Subscribe to webhooks instead of polling for state changes
