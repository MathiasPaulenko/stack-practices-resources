# Disaster Recovery Plan Template — Companion

Copy-paste assets for writing and testing a disaster recovery plan:

- `dr-plan-template.md` — the full DR plan template: RTO/RPO fields, risk scenarios, failover procedures, recovery runbook, roles, testing schedule, and communication plan.
- `failover-checklist.md` — printable checklist for running a failover drill, before/during/after.

## Usage

1. Copy `dr-plan-template.md` into your repo or wiki and fill in the bracketed fields.
2. Set RTO/RPO per service tier before writing procedures — the numbers decide the architecture, not the other way around.
3. Use `failover-checklist.md` on every drill; a drill that produces no findings isn't a real test.

Source article: <https://stackpractices.com/docs/disaster-recovery-plan-template/>
