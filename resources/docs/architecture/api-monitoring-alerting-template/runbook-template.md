# Runbook: `<Alert Name>`

> Fill this in for every page-tier alert before it goes live.
> Assume the reader is asleep, stressed, and has never seen this alert.

## Alert Condition

`<PromQL expression>` — `<threshold>` for `<duration>` (`<severity>`)

Example: `error rate > 1% for 2+ minutes (P1)`

## Quick Triage (under 60 seconds)

1. Check the dashboard: which endpoints are returning 5xx / are slowest?
2. Check recent deployments: was there a release in the last 30 minutes?
3. Check dependency health: are any upstream services down?
4. Check traffic: is volume abnormal (spike or drop)?

## Mitigation Steps

1. If a bad deployment caused it → roll back to the previous version.
2. If a dependency is down → enable the circuit breaker fallback.
3. If traffic is abnormal → enable rate limiting at the gateway.
4. If the cause is unclear → escalate to `<team/channel>` with the dashboard link.

## Verification

- [ ] Metric returned below threshold for `<X>` minutes
- [ ] No new alerts of the same type in the last `<Y>` minutes
- [ ] Error budget burn rate back to normal

## Post-Incident

1. File an incident report within 24 hours
2. Add the root cause to the known issues list
3. Update this runbook with any new triage or mitigation steps
4. If the alert fired without action needed → retune the threshold

## Links

- Dashboard: `<URL>`
- Alert rule: `<path/to/alert-rules.yml>`
- Escalation policy: `<URL>`
