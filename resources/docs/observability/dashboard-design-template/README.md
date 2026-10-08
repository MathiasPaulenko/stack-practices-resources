# Dashboard Design Template — Companion Resources

Companion files for the [Dashboard Design Template](https://stackpractices.com/docs/dashboard-design-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `dashboard-template.md` | Markdown | Full dashboard design document: layout, panel specs, SLO config, variables, annotations |
| `dashboard.json` | JSON | Importable Grafana dashboard implementing the 6-row layout with PromQL queries and thresholds |
| `slo-alerts.yml` | YAML | Prometheus rule group with fast-burn and slow-burn SLO alerts |

## Quick start

### 1. Copy the design document

```bash
cp dashboard-template.md my-service-dashboard.md
```

Replace `<Service Name>` and the `payment` placeholders with your service's data.

### 2. Import the Grafana dashboard

In Grafana: **Dashboards → New → Import → Upload JSON** and select `dashboard.json`. Pick your Prometheus data source, then update the `service="payment"` label matchers in each panel to your service name.

### 3. Load the alert rules

Add `slo-alerts.yml` to your Prometheus `rule_files` and reload:

```yaml
rule_files:
  - "slo-alerts.yml"
```

Replace `service="payment"` with your service label and point the `runbook` annotation at your real runbook URL.

## Layout reference

The dashboard reads top to bottom during an incident:

1. **Status banner** — is it broken?
2. **RED metrics** — how broken?
3. **Traffic & status codes** — where is it broken?
4. **Infrastructure** — is it resource-starved?
5. **Business metrics** — how much does it hurt?
6. **Context links** — runbooks, logs, traces.
