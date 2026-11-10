# Environment Configuration Template — Companion Resources

Fillable documentation template for capturing environment variables, endpoints, infrastructure settings, and secret locations per deployment environment.

## Files

- `environment-configuration-template.md` — blank template with all six sections
- `configmap-secret-example.yaml` — Kubernetes ConfigMap + Secret manifest showing the sensitive/non-sensitive split
- `secret-rotation-schedule.txt` — rotation schedule skeleton
- `example-filled.md` — the template filled in for a fictional payment service

## Usage

Copy `environment-configuration-template.md` into your service repository or wiki, fill in every table row for each environment, and update it in the same PR as any configuration change. Never store real secret values — record vault paths instead.

Source: https://stackpractices.com/docs/environment-configuration-template/
