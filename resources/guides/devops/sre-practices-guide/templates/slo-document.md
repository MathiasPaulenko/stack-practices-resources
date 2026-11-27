# SLO Document — [Service Name]

## SLI Definition
- Indicator: [e.g., proportion of requests with latency < 200ms]
- Measurement: [Prometheus query or data source]
- Window: [30-day rolling]

## Objective
- SLO: [e.g., 99.9% of requests < 200ms over 30 days]
- Error budget: [e.g., 0.1% = 43 minutes/month]

## Alerting
- Fast burn alert: [threshold, e.g., 14.4x burn over 1h+5m] → pages on-call
- Slow burn alert: [threshold, e.g., 6x burn over 6h+30m] → creates ticket

## Error Budget Policy
- > 50% remaining: full release velocity
- 25–50%: SRE review for risky changes
- 1–25%: freeze non-critical releases, prioritize reliability work
- Exhausted: only reliability fixes until recovery

## Ownership & Review
- Service owner: [name/team]
- Policy sign-off: [engineering + product leads]
- Review cadence: quarterly, or after any incident touching the budget
