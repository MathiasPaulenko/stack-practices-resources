# Observability Maturity Assessment — `<Team / Service>`

## Assessment Information

| Field | Value |
|-------|-------|
| Assessed By | <Name> |
| Date | 2026-07-05 |
| Team / Service | Payments Team |
| Current Score | 2.4 / 5.0 |
| Target Score | 4.0 / 5.0 |
| Target Date | 2026-10-05 |

## Maturity Levels

| Level | Name | Description |
|-------|------|-------------|
| 1 | Reactive | Logs exist but unstructured. No metrics or traces. Debugging is manual. |
| 2 | Basic | Structured logs. Key metrics collected. No tracing. Alerts are noisy. |
| 3 | Proactive | Structured logs + dashboards + distributed tracing. SLOs defined. Alerts are actionable. |
| 4 | Predictive | Anomaly detection. SLO-based alerting. Error budgets tracked. Runbooks for all alerts. |
| 5 | Autonomous | Automated remediation. Continuous profiling. Self-healing systems. Observability as code. |

## 1. Logging Assessment

| Criterion | Level | Score | Evidence | Gap |
|-----------|-------|-------|----------|-----|
| Log structure | Structured JSON | 3 | All services use `pino` with JSON output | — |
| Log levels | Used correctly | 2 | Debug logs left in production, noisy | Add log level policies |
| Correlation IDs | Present on all requests | 3 | `X-Request-ID` propagated via middleware | — |
| Log retention | 30 days hot, 90 cold | 3 | ELK stack with ILM policies | — |
| Log searchability | Queryable by field | 3 | Elasticsearch with structured fields | — |
| Sensitive data | Scrubbed before logging | 2 | Some endpoints log full request bodies | Add PII redaction filter |
| **Logging Average** | | **2.7** | | |

### Logging Gaps

| Gap | Current | Target | Action | Effort |
|-----|---------|--------|--------|--------|
| Debug logs in production | Level 2 | Level 3 | Set production log level to `info`, remove debug statements | 1 day |
| PII in request logs | Level 2 | Level 4 | Add redaction filter for email, phone, SSN fields | 2 days |
| No log-based alerts | Level 2 | Level 3 | Create alerts for error log spikes per service | 1 day |

## 2. Metrics Assessment

| Criterion | Level | Score | Evidence | Gap |
|-----------|-------|-------|----------|-----|
| RED metrics (Rate, Errors, Duration) | Collected for all services | 3 | Prometheus + custom exporters | Add duration histograms for 2 services |
| USE metrics (Utilization, Saturation, Errors) | Collected for infrastructure | 3 | Node exporter, cAdvisor | — |
| Business metrics | Order count, revenue, conversion | 2 | Some metrics in Mixpanel, not in Prometheus | Expose business metrics from app |
| Metric cardinality | Controlled | 2 | Some high-cardinality labels (user_id) | Remove user_id labels, use exemplars |
| Dashboards | Per-service dashboards | 3 | Grafana dashboards for each service | Add business metrics dashboard |
| SLO dashboards | Defined and tracked | 1 | No SLOs defined | Define SLOs for payment service |
| **Metrics Average** | | **2.3** | | |

### Metrics Gaps

| Gap | Current | Target | Action | Effort |
|-----|---------|--------|--------|--------|
| No SLOs | Level 1 | Level 4 | Define SLOs: 99.9% availability, p95 < 500ms | 3 days |
| High cardinality labels | Level 2 | Level 3 | Remove user_id from metrics, use traces for per-user analysis | 1 day |
| Missing business metrics | Level 2 | Level 3 | Expose order_count, revenue_total, conversion_rate from app | 2 days |
| No latency histograms | Level 2 | Level 3 | Replace counter-based duration with Prometheus histograms | 1 day |

## 3. Tracing Assessment

| Criterion | Level | Score | Evidence | Gap |
|-----------|-------|-------|----------|-----|
| Distributed tracing | Implemented | 2 | OpenTelemetry SDK in 3 of 8 services | Instrument remaining services |
| Trace propagation | W3C trace context | 3 | `traceparent` header propagated | — |
| Span attributes | Standardized | 2 | Some services have rich spans, others minimal | Add span attributes for DB queries |
| Trace sampling | Head-based + tail-based | 2 | Head-based at 10%, no tail-based | Add tail-based sampling for errors |
| Trace correlation | Linked to logs and metrics | 2 | trace_id in logs, but not in metrics | Add exemplars linking traces to metrics |
| Service maps | Auto-generated | 3 | Service mesh generates dependency map | — |
| **Tracing Average** | | **2.3** | | |

### Tracing Gaps

| Gap | Current | Target | Action | Effort |
|-----|---------|--------|--------|--------|
| 5 services not instrumented | Level 2 | Level 4 | Add OpenTelemetry SDK to remaining 5 services | 5 days |
| No tail-based sampling | Level 2 | Level 4 | Deploy OpenTelemetry Collector with tail-based sampling | 2 days |
| Missing DB span attributes | Level 2 | Level 3 | Add db.system, db.statement, db.operation attributes | 1 day |
| No trace-to-metric exemplars | Level 2 | Level 4 | Configure Prometheus exemplars linking to trace IDs | 2 days |

## 4. Alerting Assessment

| Criterion | Level | Score | Evidence | Gap |
|-----------|-------|-------|----------|-----|
| Alert noise | Low false positive rate | 2 | ~40% of alerts are actionable | Tune alert thresholds, remove noisy alerts |
| Alert routing | Routed to correct team | 3 | Alertmanager routes by service label | — |
| Runbooks | Linked to alerts | 1 | Most alerts have no runbook | Create runbooks for top 20 alerts |
| SLO-based alerting | Multi-window burn rate | 1 | No SLO-based alerts | Implement SLO-based alerting once SLOs defined |
| Alert escalation | Defined escalation policy | 3 | PagerDuty with 3-level escalation | — |
| Alert context | Includes dashboard links, logs | 2 | Some alerts include Grafana links | Add runbook and log links to all alerts |
| **Alerting Average** | | **2.0** | | |

### Alerting Gaps

| Gap | Current | Target | Action | Effort |
|-----|---------|--------|--------|--------|
| No runbooks | Level 1 | Level 4 | Write runbooks for top 20 alerts | 5 days |
| 60% false positives | Level 2 | Level 4 | Audit all alerts, tune or remove noisy ones | 3 days |
| No SLO-based alerting | Level 1 | Level 4 | Implement multi-window burn rate alerts | 3 days |
| Missing alert context | Level 2 | Level 3 | Add runbook URL, dashboard URL, log query to alert annotations | 1 day |

## 5. Culture and Process Assessment

| Criterion | Level | Score | Evidence | Gap |
|-----------|-------|-------|----------|-----|
| Observability ownership | Each team owns their dashboards | 3 | Teams create and maintain their own dashboards | — |
| Incident review | Postmortems for all incidents | 3 | Blameless postmortems within 48 hours | — |
| Action item tracking | Tracked to completion | 2 | Action items created but ~40% overdue | Add monthly action item review |
| On-call culture | Sustainable rotation | 3 | 1-week rotation, 3 engineers, follow-the-sun | — |
| Observability training | New hires trained | 1 | No formal onboarding for observability tools | Create observability onboarding guide |
| **Culture Average** | | **2.4** | | |

### Culture Gaps

| Gap | Current | Target | Action | Effort |
|-----|---------|--------|--------|--------|
| No observability onboarding | Level 1 | Level 3 | Create onboarding guide for logging, metrics, tracing tools | 2 days |
| Action items overdue | Level 2 | Level 4 | Monthly review of postmortem action items, assign owners | 0.5 days |

## 6. Aggregated Score

| Dimension | Score | Target | Gap |
|-----------|-------|--------|-----|
| Logging | 2.7 | 4.0 | 1.3 |
| Metrics | 2.3 | 4.0 | 1.7 |
| Tracing | 2.3 | 4.0 | 1.7 |
| Alerting | 2.0 | 4.0 | 2.0 |
| Culture | 2.4 | 4.0 | 1.6 |
| **Aggregate** | **2.3** | **4.0** | **1.7** |

## 7. Improvement Roadmap

| Quarter | Initiative | Dimension | Target Level | Effort | Owner |
|---------|-----------|-----------|-------------|--------|-------|
| Q3 2026 | Define SLOs for all critical services | Metrics | 3→4 | 3 days | SRE |
| Q3 2026 | Instrument remaining 5 services with OTel | Tracing | 2→4 | 5 days | Platform |
| Q3 2026 | Write runbooks for top 20 alerts | Alerting | 1→4 | 5 days | Each team |
| Q3 2026 | Audit and tune noisy alerts | Alerting | 2→4 | 3 days | SRE |
| Q4 2026 | Implement tail-based sampling | Tracing | 2→4 | 2 days | Platform |
| Q4 2026 | Add PII redaction to logs | Logging | 2→4 | 2 days | Platform |
| Q4 2026 | Create observability onboarding guide | Culture | 1→3 | 2 days | SRE |
| Q4 2026 | Implement SLO-based alerting | Alerting | 1→4 | 3 days | SRE |
| Q1 2027 | Add business metrics to Prometheus | Metrics | 2→3 | 2 days | Backend |
| Q1 2027 | Monthly action item review process | Culture | 2→4 | 0.5 days | Eng Manager |
