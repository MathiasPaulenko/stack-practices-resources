# Escalation Policy Template Resources

Companion resources for [Escalation Policy Template](https://stackpractices.com/docs/escalation-policy-template/).

## Files

| File | Description |
|------|-------------|
| `policy/escalation-policy-template.md` | Fill-in policy document: severity matrix, L1–L4 roster, timed escalation paths, comms channels, unresponsive-responder rules, and maintenance duties |
| `config/pagerduty-escalation-policy.yaml` | PagerDuty-style escalation policies for SEV 1 and SEV 2, with notes on the `escalation_delay_in_minutes` and `num_loops` semantics |
| `config/opsgenie-escalation.json` | Opsgenie-style escalation payload (`if-not-acked` rules with timed delays and repeat) ready to adapt to your schedules |
| `templates/incident-communications.md` | Copy-paste notices for every stage: initial customer notice, progress update, resolution, internal escalation ping, and executive summary |
| `templates/post-incident-review.md` | Post-incident review template with a dedicated escalation-review section that feeds rule changes back into the policy |
| `checklists/escalation-drill.md` | Quarterly drill checklist: walk the ladder with a synthetic alert and verify every phone number, delay, and channel |

## Usage

1. Copy `policy/escalation-policy-template.md`, fill in your roster, SLAs, and channels, and commit it next to your runbooks.
2. Translate the policy into your paging tool using `config/` as the reference — mind that the delay on a rule is that level's timeout, not a wait before the first page.
3. Keep `templates/incident-communications.md` pinned in your incidents channel for SEV 1–2.
4. Run `checklists/escalation-drill.md` every quarter; contact data goes stale silently.
