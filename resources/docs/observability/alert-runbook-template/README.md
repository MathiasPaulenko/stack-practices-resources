# Alert Runbook Template — Companion Files

Downloadable files for the [Alert Runbook Template](https://stackpractices.com/docs/alert-runbook-template/) on StackPractices.

- `alert-runbook-template.md` — blank fillable template with placeholders for every section (metadata, triage, diagnosis branches, mitigation, escalation, resolution, post-incident).
- `runbook-high-error-rate-example.md` — worked example: the same template filled in for a payment-service error-rate alert (Prometheus + Kubernetes).

Copy the blank file next to your alerting rules, fill one runbook per alert, and link it from the alert's `runbook_url` annotation.
