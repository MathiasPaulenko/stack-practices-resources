# First-Minute Triage Checklist

When paged, answer these questions in order before touching anything:

1. **What is failing?** — service name, endpoint, region
2. **Who is affected?** — all users, a subset, internal only?
3. **When did it start?** — exact time of first failure (check deployment logs)
4. **What changed?** — any deploy, config change, or dependency shift?
5. **Is it getting worse?** — trend of error rate over time

Then:

- [ ] Declare severity (SEV-1 to SEV-4)
- [ ] Open or join the incident channel
- [ ] Post the first status update
- [ ] Escalate to secondary if SEV-1/SEV-2 and no progress in 15-20 min
