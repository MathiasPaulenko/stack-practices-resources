# Worked Example: SEV-1 Checkout Outage

Condensed timeline from the e-commerce scenario in the guide.

```
14:12 - Alert fires: CheckoutErrorRate 100%
14:13 - Primary receives page
14:16 - SEV-1 declared, bridge opened
14:17 - Secondary + service owner invited
14:18 - Recent deploy found (v2.4, 8 min ago)
14:20 - Secondary confirms DB pool exhausted
14:23 - Rollback to v2.3 executed
14:26 - Service restored
14:35 - Resolved; postmortem ticket created
```

Roles: IC coordinates (does not debug), Communications updates stakeholders,
SME investigates, Scribe keeps the timeline.
