# API Monitoring & Alerting Template — Companion

Ready-to-import companion files for the [API Monitoring & Alerting Template](https://stackpractices.com/docs/api-monitoring-alerting-template/) doc: Prometheus alert rules with fast/slow burn rate, a Grafana dashboard JSON, and a fill-in runbook template.

## Files

| File | What it is |
|------|-----------|
| `alert-rules.yml` | Prometheus rules for the page tier (P0/P1), warning tier, and SLO burn rate — load via `rule_files` |
| `grafana-dashboard.json` | 6-panel dashboard: availability gauge, error rate, burn rate, rps, latency heatmap, error timeline |
| `runbook-template.md` | Fill-in runbook: alert condition → 60s triage → mitigation → verification → post-incident |

## Quick start

```bash
# 1. Alert rules — point prometheus.yml at the file
#    rule_files:
#      - "alert-rules.yml"
promtool check rules alert-rules.yml   # validate before loading

# 2. Dashboard — Grafana → Dashboards → New → Import → paste grafana-dashboard.json

# 3. Runbook — copy runbook-template.md per alert, fill <placeholders>,
#    and set the runbook annotation in alert-rules.yml to its URL
```

## Adapt to your metrics

The rules assume standard instrumentation: `http_requests_total{status}` counter and `http_request_duration_seconds_bucket` histogram (OpenTelemetry collector, ingress-nginx, and most HTTP middlewares emit these). If your labels differ — e.g. `code` instead of `status` — grep-replace in both the rules and the dashboard before importing.

Calibrate thresholds using the doc's "Choosing Thresholds" section: baseline 2–4 weeks, set page thresholds at ~2x baseline, warnings at ~1.3x.

## References

- Doc: https://stackpractices.com/docs/api-monitoring-alerting-template/
- Google SRE — Monitoring Distributed Systems: https://sre.google/sre-book/monitoring-distributed-systems/
- Google SRE Workbook — Alerting on SLOs: https://sre.google/workbook/alerting-on-slos/
- Prometheus alerting rules: https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/
