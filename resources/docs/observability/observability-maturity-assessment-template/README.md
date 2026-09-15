# Observability Maturity Assessment — Companion Resources

Companion files for the [Observability Maturity Assessment Template](https://stackpractices.com/docs/observability-maturity-assessment-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `assessment-template.md` | Markdown | Full assessment template with 5 dimensions, scoring, gaps, and roadmap |
| `scoring-sheet.csv` | CSV | Spreadsheet-ready scoring data for all 5 dimensions and 30 criteria |

## Quick start

### 1. Copy the assessment template

```bash
cp assessment-template.md my-team-assessment.md
```

Edit `my-team-assessment.md` and replace `<Team / Service>`, `<Name>`, and placeholder values with your team's data.

### 2. Import scoring sheet

Open `scoring-sheet.csv` in Excel, Google Sheets, or any CSV editor to track scores across dimensions.

## Assessment structure

1. **Logging** — structure, levels, correlation IDs, retention, searchability, sensitive data
2. **Metrics** — RED/USE metrics, business metrics, cardinality, dashboards, SLOs
3. **Tracing** — distributed tracing, propagation, span attributes, sampling, correlation
4. **Alerting** — noise, routing, runbooks, SLO-based alerting, escalation, context
5. **Culture** — ownership, incident review, action items, on-call, training

## Maturity levels

| Level | Name | Description |
|-------|------|-------------|
| 1 | Reactive | Logs unstructured, no metrics/traces, manual debugging |
| 2 | Basic | Structured logs, key metrics, no tracing, noisy alerts |
| 3 | Proactive | Logs + dashboards + tracing, SLOs, actionable alerts |
| 4 | Predictive | Anomaly detection, SLO alerting, error budgets, runbooks |
| 5 | Autonomous | Automated remediation, continuous profiling, self-healing |

## References

- [Google SRE Workbook](https://sre.google/workbook/)
- [OpenTelemetry](https://opentelemetry.io/)
- [Prometheus monitoring](https://prometheus.io/docs/introduction/overview/)
