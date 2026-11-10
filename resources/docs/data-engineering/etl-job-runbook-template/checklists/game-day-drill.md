# Game day drill — testing the ETL runbook

Run quarterly for critical pipelines. One person injects the failure, another (who hasn't seen the plan) resolves it using only the runbook.

## Before

- [ ] Pick one failure scenario from section 4 of the runbook
- [ ] Confirm the drill runs in staging or a shadow pipeline, never production
- [ ] Have a rollback path for the injected failure ready before starting
- [ ] Timebox: the drill ends at the SLA boundary even if unresolved

## Scenarios (pick one)

- [ ] **Auth failure**: revoke the source API token in the dev secrets manager → expect F1 path
- [ ] **Rate limit**: point the extractor at a mock endpoint that returns 429 → expect F2 path
- [ ] **dbt break**: rename a staging column → expect F3 diagnosis
- [ ] **Quality gate**: seed rows violating a `not_null` test → expect F4 triage
- [ ] **Volume spike**: run the pipeline against a 10x fixture → expect F6 SLA behavior

## During — evaluator scores

- [ ] Operator found the right failure entry without prompting
- [ ] Followed diagnostic steps in order, no skipped checks
- [ ] Commands ran as written (no stale flags, no typos in the runbook)
- [ ] Expected outputs matched reality
- [ ] Escalation path used at the right timeout (or correctly not used)
- [ ] Time to resolution within the failure's expected window

## After

- [ ] Every wrong or missing step becomes a runbook update in the same PR
- [ ] Commands that needed "interpretation" get rewritten to be copy-paste exact
- [ ] New failure mode discovered? Add it as F(n+1) with the full template block
- [ ] Log the drill in the runbook's history (date, scenario, gaps found)
