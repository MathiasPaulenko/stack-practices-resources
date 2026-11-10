# Quarterly Escalation Drill Checklist

Run at a reasonable hour once per quarter. Goal: prove the whole chain works before a real incident does.

## Before the drill

- [ ] Announce the drill in the team channel (nobody should think it's a real SEV 1)
- [ ] Pick the person who will deliberately not ack the first page (the "sleeping primary")
- [ ] Have the policy document open — you're validating the tool against the document

## Walk the ladder

- [ ] Trigger a synthetic SEV 1 alert against a non-production or test service
- [ ] Confirm the L1 page arrives on the primary's device (push + SMS + phone call if configured)
- [ ] Let the L1 timeout elapse — confirm the backup gets paged automatically
- [ ] Confirm the L2 page fires at the documented delay, on the documented channel
- [ ] Confirm each notification contains service name, severity, and a link to the runbook
- [ ] Resolve the test incident and confirm the escalation chain stops

## Verify the data

- [ ] Every phone number in the roster still rings
- [ ] Backup responders know they are the backup this week
- [ ] Handoff times in the tool match the written policy
- [ ] Policy `num_loops` / repeat setting matches the document (not the tool default)

## After the drill

- [ ] Fix every gap found the same day — stale contact data is a real incident waiting
- [ ] Log the drill date and findings in the policy document's maintenance section
- [ ] Update `lastReviewed` / version in the policy header
