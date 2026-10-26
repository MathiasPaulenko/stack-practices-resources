# Hypothesis Template

**We believe** that [change]
**will result in** [metric improvement]
**for** [user segment]
**because** [reasoning based on data/observation]

## Example

We believe that reducing checkout steps from 5 to 3
will result in a 5% increase in checkout completion rate
for mobile users
because analytics show 40% drop-off at step 4 on mobile.

## Pre-launch checklist

- Primary metric — the single metric that decides the experiment. One, not three.
- Guardrail metrics — things that must not degrade (error rate, p95 latency, refund rate). Define kill thresholds upfront.
- Target population — which users are eligible and how logged-out traffic is handled.
- MDE — the smallest lift worth shipping.
- Duration — a fixed end date covering full weekly cycles, decided before looking at any data.
