# SRE Practices Guide — Companion Kit

Companion material for [Site Reliability Engineering](https://stackpractices.com/guides/sre-practices-guide/).

## Contents

| File | Description |
|------|-------------|
| `alerting/burn-rate-alerts.yml` | Prometheus alerting rules: multi-window burn rate for a 99.9% SLO (page + ticket tiers) |
| `templates/slo-document.md` | Fill-in SLO document: SLI definition, objective, alerting, error budget policy |
| `templates/postmortem-template.md` | Blameless postmortem template with timeline, contributing factors, and action items |

## Usage

1. Copy `burn-rate-alerts.yml` into your Prometheus rules directory and adjust the multipliers (14.4x / 6x) and the error ratio base (0.001 for a 99.9% SLO) to match your target.
2. Fill in `slo-document.md` per service and get sign-off from engineering and product — a budget policy nobody signed doesn't stop launches.
3. Use `postmortem-template.md` for every incident that touches the error budget; review open action items weekly.
