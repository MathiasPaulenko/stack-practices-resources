# On-Call Runbook Template Resources

Companion resources for [On-Call Runbook Template](https://stackpractices.com/docs/on-call-runbook-template/).

## Files

| File | Description |
|------|-------------|
| `runbook/on-call-runbook-template.md` | Alert-indexed runbook template: seven response procedures with symptoms, diagnostic steps, resolution, and escalation — including the Do-NOT anti-patterns list |
| `scripts/diagnose.sh` | Executable diagnostic collector: gathers service status, logs, resources, network, deployments, and a health check into a timestamped report |
| `monitoring/prometheus-alerts.yml` | Prometheus alert rules wired to runbook sections via `runbook:` and `dashboard:` annotations |
| `monitoring/kubectl-diagnostics.md` | Kubernetes diagnostic one-liners for pod status, logs, events, and network debugging |
| `checklists/post-incident-update.md` | Post-incident checklist that keeps the runbook updated after every incident |

## Usage

1. Copy `runbook/on-call-runbook-template.md`, fill in your service name, and map your real alerts to sections.
2. Make `scripts/diagnose.sh` executable (`chmod +x`) and keep it on the box your on-call engineers log into.
3. Adapt `monitoring/prometheus-alerts.yml` to your metrics — the `runbook:` annotation is what links the page to the procedure.
4. Run `checklists/post-incident-update.md` after every incident so the runbook absorbs what it learned.
