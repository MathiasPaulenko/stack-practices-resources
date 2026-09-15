# SLO Document Template — Companion Resources

Companion files for the [SLO Document Template](https://stackpractices.com/docs/slo-document-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `slo-template.md` | Markdown | Copy-paste ready SLO document with SLIs, SLOs, error budgets, dependencies |
| `slo-alerts.yaml` | YAML | Prometheus alerting rules for SLO burn rate and latency breaches |

## Quick start

### 1. Copy the template

```bash
cp slo-template.md my-service-slo.md
```

Edit `my-service-slo.md` and replace `[Service Name]`, `[team]`, and placeholder values.

### 2. Deploy alerting rules

Edit `slo-alerts.yaml` and replace `[service]` with your Prometheus job name:

```bash
# Copy to Prometheus rules directory
cp slo-alerts.yaml /etc/prometheus/rules/slo-alerts.yaml

# Reload Prometheus
curl -X POST http://localhost:9090/-/reload
```

## Template structure

1. **Overview** — service name, owner, review date
2. **SLIs** — availability, latency, throughput measurements
3. **SLOs** — targets with measurement windows
4. **Error Budget** — budget calculation and policy
5. **Alerting Thresholds** — page vs ticket severity
6. **Dependencies** — upstream services and their SLOs
7. **SLI Selection Guide** — good vs bad SLIs by service type
8. **Review Notes** — quarterly review checklist

## References

- [Google SRE Workbook](https://sre.google/workbook/table-of-contents/)
- [Prometheus alerting best practices](https://prometheus.io/docs/practices/alerting/)
