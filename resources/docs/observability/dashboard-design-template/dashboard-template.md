````markdown
# Dashboard Design: `<Service Name>`

## Dashboard Metadata

| Field | Value |
|-------|-------|
| Dashboard Title | Payment Service Health |
| Dashboard URL | https://grafana.example.com/d/payment-service |
| Owner | Payment Team |
| Last Reviewed | 2026-07-05 |
| Audience | On-call engineers, developers, SRE |
| Refresh Interval | 30 seconds |
| Time Range Default | Last 1 hour |

## 1. Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│  ROW 1: Service Status Banner                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Health      │  │ SLO Status  │  │ Error Budget│         │
│  │ OK/WARN/ERR │  │ 99.9%       │  │ 72% remain  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ROW 2: RED Metrics (Rate, Errors, Duration)                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Request Rate│  │ Error Rate  │  │ p95 Latency │         │
│  │ (req/s)     │  │ (% of total)│  │ (ms)        │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ROW 3: Traffic and Status Codes                             │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  │
│  │ Requests by endpoint    │  │ Status code distribution│  │
│  │ (stacked area)          │  │ (pie chart)             │  │
│  └─────────────────────────┘  └─────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ROW 4: Infrastructure Health                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ CPU Usage   │  │ Memory      │  │ DB Conns    │         │
│  │ (%)         │  │ (MB)        │  │ (active/idle)│        │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ROW 5: Business Metrics                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Orders/min  │  │ Revenue/min │  │ Success Rate│         │
│  │             │  │ ($)         │  │ (%)         │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ROW 6: Context and Links                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Runbook | Logs | Traces | Alerts | Deploy Info     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 2. Panel Specifications

### Row 1: Service Status Banner

| Panel | Type | Query | Thresholds | Purpose |
|-------|------|-------|------------|---------|
| Health | Stat | `up{service="payment"}` | OK: 1, WARN: 0.5, ERR: 0 | Quick health check |
| SLO Status | Stat | `payment_slo_availability_ratio` | OK: > 0.999, WARN: > 0.99, ERR: < 0.99 | SLO compliance at a glance |
| Error Budget | Gauge | `payment_error_budget_remaining_pct` | OK: > 30%, WARN: > 10%, ERR: < 10% | How much error budget is left |

### Row 2: RED Metrics

| Panel | Type | Query | Thresholds | Purpose |
|-------|------|-------|------------|---------|
| Request Rate | Time series | `rate(http_requests_total{service="payment"}[5m])` | — | Traffic volume |
| Error Rate | Time series | `rate(http_requests_total{service="payment",status=~"5.."}[5m]) / rate(http_requests_total{service="payment"}[5m])` | WARN: > 1%, ERR: > 5% | Error percentage |
| p95 Latency | Time series | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{service="payment"}[5m]))` | WARN: > 500ms, ERR: > 1s | Response time |

### Row 3: Traffic and Status Codes

| Panel | Type | Query | Purpose |
|-------|------|-------|---------|
| Requests by endpoint | Stacked area | `sum(rate(http_requests_total{service="payment"}[5m])) by (endpoint)` | See traffic distribution |
| Status code distribution | Pie chart | `sum(rate(http_requests_total{service="payment"}[5m])) by (status)` | Spot error patterns |

### Row 4: Infrastructure Health

| Panel | Type | Query | Thresholds | Purpose |
|-------|------|-------|------------|---------|
| CPU Usage | Time series | `rate(container_cpu_usage_seconds_total{pod=~"payment.*"}[5m]) * 100` | WARN: > 70%, ERR: > 90% | Resource saturation |
| Memory | Time series | `container_memory_working_set_bytes{pod=~"payment.*"}` | WARN: > 80% limit, ERR: > 95% | Memory pressure |
| DB Connections | Time series | `payment_db_connections_active` / `payment_db_connections_max` | WARN: > 70%, ERR: > 90% | Pool exhaustion |

### Row 5: Business Metrics

| Panel | Type | Query | Thresholds | Purpose |
|-------|------|-------|------------|---------|
| Orders/min | Time series | `rate(payment_orders_total[5m]) * 60` | — | Business throughput |
| Revenue/min | Time series | `rate(payment_revenue_total[5m]) * 60` | — | Revenue tracking |
| Success Rate | Stat | `rate(payment_orders_total{status="success"}[5m]) / rate(payment_orders_total[5m])` | WARN: < 99%, ERR: < 95% | Business health |

### Row 6: Context and Links

| Link | URL | Purpose |
|------|-----|---------|
| Runbook | https://runbooks.example.com/payment-service | Incident response |
| Logs | https://kibana.example.com/app/discover#/?_a=(query:service:payment) | Log search |
| Traces | https://jaeger.example.com/search?service=payment | Distributed traces |
| Alerts | https://alertmanager.example.com/#/alerts?receiver=payment | Active alerts |
| Deploy Info | https://grafana.example.com/d/deployments?service=payment | Recent deployments |

## 3. SLO Configuration

### SLO Definition

| SLO | Target | Window | Error Budget | Measurement |
|-----|--------|--------|-------------|-------------|
| Availability | 99.9% | 30 days | 0.1% = 43.2 min | `1 - (failed_requests / total_requests)` |
| Latency p95 | < 500ms | 30 days | 0.1% = 43.2 min | `histogram_quantile(0.95, ...)` |
| Latency p99 | < 2s | 30 days | 0.1% = 43.2 min | `histogram_quantile(0.99, ...)` |

### Error Budget Tracking

| Metric | Query | Purpose |
|--------|-------|---------|
| Budget remaining | `1 - (rate(errors[30d]) / 0.001)` | How much budget is left |
| Burn rate (1h) | `rate(errors[1h]) / 0.001` | Fast burn detection |
| Burn rate (6h) | `rate(errors[6h]) / 0.001` | Sustained burn detection |
| Budget reset date | `30d - elapsed_in_window` | When budget resets |

### Alerting Rules

```yaml
- alert: PaymentSLOFastBurn
  expr: |
    (
      sum(rate(http_requests_total{service="payment",status=~"5.."}[1h]))
      /
      sum(rate(http_requests_total{service="payment"}[1h]))
    ) > 0.02
  for: 5m
  labels:
    severity: critical
    service: payment
  annotations:
    summary: "Payment SLO fast burn — 2% budget consumed in 1h"
    runbook: "https://runbooks.example.com/payment-slo-burn"

# Slow burn: 5% of budget in 6 hours
- alert: PaymentSLOSlowBurn
  expr: |
    (
      sum(rate(http_requests_total{service="payment",status=~"5.."}[6h]))
      /
      sum(rate(http_requests_total{service="payment"}[6h]))
    ) > 0.005
  for: 30m
  labels:
    severity: warning
    service: payment
  annotations:
    summary: "Payment SLO slow burn — 5% budget consumed in 6h"
    runbook: "https://runbooks.example.com/payment-slo-burn"
```

## 4. Dashboard Variables

| Variable | Type | Query | Default | Purpose |
|----------|------|-------|---------|---------|
| $datasource | Data source | — | Prometheus | Switch between environments |
| $environment | Query | `label_values(up, environment)` | production | Filter by environment |
| $instance | Query | `label_values(up{service="payment"}, instance)` | All | Filter by instance |
| $endpoint | Query | `label_values(http_requests_total{service="payment"}, endpoint)` | All | Filter by endpoint |
| $timeframe | Interval | — | 1h | Quick time range switch |

## 5. Annotation Layers

| Annotation | Query | Purpose |
|------------|-------|---------|
| Deployments | `deployments{service="payment"}` | Correlate changes with metric shifts |
| Incidents | `incidents{service="payment"}` | See incident impact on metrics |
| Maintenance | `maintenance{service="payment"}` | Expected dips during maintenance |
| Alerts | `alerts{service="payment"}` | When alerts fired relative to metrics |
````
