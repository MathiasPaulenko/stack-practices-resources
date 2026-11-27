# SLA Definition Template — Companion Files

Companion files for the [SLA Definition Template](https://stackpractices.com/docs/sla-definition-template/)
on StackPractices. Everything here is copy-paste ready: fill in the
placeholders, adjust the numbers to your service, and adapt the policies
to your team's operating model.

## Files

| File | Purpose |
|------|---------|
| `sla-template.md` | Complete SLA document template (EN) with SLOs, SLIs, error budget, severity matrix, exclusions, credits, communication plan and review cadence |
| `sla-template.es.md` | Same template in Spanish |
| `prometheus-slo-rules.yaml` | Prometheus recording rules (availability, error budget remaining, multi-window burn rate) plus alert rules for 2x/10x burn and exhausted budget |
| `burn_rate.py` | Runnable Python calculator: computes burn rate, remaining budget percentage and the recommended deploy-policy action |

## Quick Start

1. Copy `sla-template.md` into your docs repo and replace the
   placeholders (`<Service Name>`, dates, team, measurement source).
2. Set targets from measured behavior — run the service for a month
   first, then tighten the numbers slightly.
3. Load `prometheus-slo-rules.yaml` via `rule_files` in your Prometheus
   config and adjust the `0.999` target and window sizes.
4. Sanity-check budgets with the calculator:

```bash
python burn_rate.py
# Burn rate: 13.9x
# Budget remaining: 95.4%
# Action: ship freely
```

## Notes

- Keep the measurement source named in the SLA — whoever owns the
  numbers owns the argument in a dispute.
- Exclusions work only when they are precise ("up to 4 hours/month
  with 7 days notice"), not open-ended.
- The burn-rate alerts use multi-window detection (5m + 1h) to avoid
  paging on short spikes.

Source: <https://stackpractices.com/docs/sla-definition-template/>
