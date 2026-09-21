# Monitoring & Alerting Policy — Companion Resources

Companion files for the [Monitoring and Alerting Policy Template](https://stackpractices.com/docs/monitoring-alerting-policy-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `prometheus-alert-rules.yaml` | YAML | Alert rules with `severity` (P1–P5) and `team` labels matching the policy — error rate, latency, disk, and certificate expiry |
| `alertmanager-routing.yaml` | YAML | Routing tree that maps severity to channels (PagerDuty / Slack / email) with escalation-friendly `repeat_interval` values and a P1→P2 inhibit rule |
| `alert-quality-scorecard.md` | Markdown | Printable scorecard for the quarterly alert review, with interpretation bands and a review log |

## Quick start

### 1. Adapt the alert rules

Replace the example thresholds with values calibrated to your last 90 days of metrics, then point each `runbook` annotation at a real runbook URL. Load the rules into Prometheus:

```bash
promtool check rules prometheus-alert-rules.yaml
```

### 2. Adapt the routing config

Replace `P1_SERVICE_KEY`, `P2_SERVICE_KEY`, `SLACK_WEBHOOK_URL`, and the email target with real credentials, then validate:

```bash
amtool check-config alertmanager-routing.yaml
```

### 3. Run the quarterly review

Copy `alert-quality-scorecard.md` per alert or per team, score the six criteria, and apply the interpretation bands: below 12 delete, 12–17 improvement plan, 18+ healthy.

## Placeholders

| Placeholder | Replace with |
|-------------|--------------|
| `P1_SERVICE_KEY` / `P2_SERVICE_KEY` | PagerDuty integration keys |
| `SLACK_WEBHOOK_URL` | Incoming webhook URL |
| `team@example.com` | Team mailing list |
| `runbooks.example.com` | Your runbook base URL |
