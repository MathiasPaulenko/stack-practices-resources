# Engineering Handbook: `<Team/Company Name>`

> Last updated: ______ | Owner: ______ | Questions: #engineering-help

---

## 1. Our Philosophy

### Mission
[One sentence describing what the engineering team exists to achieve]

### Principles
1. **______** — [Explanation and what it means in practice]
2. **______** — [Explanation]
3. **______** — [Explanation]

### What We Value
| Value | What It Looks Like | What It Does Not Look Like |
|-------|--------------------|---------------------------|
| Quality | Writing tests before shipping; fixing root causes | Shipping untested code; applying band-aids |
| Speed | Small PRs; fast feedback; removing blockers | Rushing; skipping review; building without planning |
| Collaboration | Pairing; knowledge sharing; respectful debate | Silos; blame; gatekeeping information |
| Ownership | Fixing what you break; monitoring what you ship | Throwing code over the wall; ignoring alerts |

---

## 2. How We Work

### Communication
| Channel | Use For | Response Time | Notes |
|---------|---------|---------------|-------|
| Slack #engineering | General discussion; quick questions | Same day | Public by default |
| Slack DMs | Private or sensitive topics | Same day | Use sparingly |
| Email | External communication; formal announcements | 24 hours | |
| GitHub PR comments | Code-specific discussion | During review | Keep technical |
| Video call | Complex discussions; kickoffs; 1:1s | Scheduled | Record if others need it |

### Meetings
| Meeting | Frequency | Duration | Required | Purpose |
|---------|-----------|----------|----------|---------|
| Standup | Daily | 15 min | All | Blockers and coordination |
| Sprint Planning | Weekly/Biweekly | 60 min | All | Commit to upcoming work |
| Retro | Weekly/Biweekly | 45 min | All | Process improvement |
| 1:1 | Weekly | 30 min | Manager + IC | Growth and support |
| Tech Talk | Monthly | 30 min | Voluntary | Knowledge sharing |

### Working Hours and Availability
- Core collaboration hours: ______ to ______ [timezone]
- Flexible hours outside core time
- On-call engineers must be available within 15 minutes during shifts
- Meeting-free focus blocks: ______ [when]

---

## 3. Development Workflow

### Our Process
1. **Pick up work** — Self-assign from ready column in [ticket system]
2. **Start a branch** — Follow the branching strategy doc
3. **Write code + tests** — All code must have tests; all tests must pass
4. **Open PR** — Fill out PR template; request review from [team members]
5. **Address feedback** — Discuss, iterate, resolve
6. **Merge** — Only after approval + CI green; merge using [merge strategy]
7. **Deploy** — Follow deployment checklist; monitor after release
8. **Verify** — Confirm in production; close ticket

### Definition of Done
- [ ] Code written and tested locally
- [ ] Unit tests added/updated with >80% coverage
- [ ] Integration tests pass
- [ ] Code reviewed and approved by [number] engineer(s)
- [ ] Documentation updated (API docs, README, runbooks)
- [ ] Monitoring and alerts added for new functionality
- [ ] Deployed to production
- [ ] Verified working in production
- [ ] Ticket closed with resolution notes

### Code Review Standards
- Review within [timeframe] of PR opening
- Approvals required from [number] non-author engineer(s)
- Review for: correctness, maintainability, security, performance, test coverage
- Nitpicks: prefix with "Nit:"; the author decides whether to address
- Blockers: must be resolved before merge
- If you don't understand something, ask — silence is not approval

---

## 4. Technical Standards

### Languages and Frameworks
| Layer | Primary | Approved Alternatives | Deprecated |
|-------|---------|----------------------|------------|
| Backend | ______ | ______ | ______ |
| Frontend | ______ | ______ | ______ |
| Mobile | ______ | ______ | ______ |
| Database | ______ | ______ | ______ |
| Cache | ______ | ______ | ______ |
| Queue | ______ | ______ | ______ |

### Architecture Principles
1. **______** — [Example and rationale; link to the ADR that decided it]
2. **______** — [Example and rationale]
3. **______** — [Example and rationale]

### Security Requirements
- All services authenticate and authorize requests
- Secrets never committed to code; use the secret manager
- Dependencies scanned for vulnerabilities weekly
- Encryption in transit (TLS 1.2+) and at rest for sensitive data
- Security review required for auth, payment and data-handling changes

### Observability Standards
- All services export metrics (RED: Rate, Errors, Duration)
- All errors logged in structured format with correlation IDs
- All services expose health check endpoints
- Alerts defined before shipping new capabilities
- A dashboard exists for every service

---

## 5. Operational Practices

### On-Call
- Rotation: ______
- Handoff: every [frequency] using the on-call handoff template
- Response time: P1 = 15 min, P2 = 30 min, P3 = 2 hours
- Escalation: after [time] without acknowledgment
- Compensation: ______ [if applicable]

### Incident Response
1. Acknowledge the page within the SLA
2. Declare the incident in #incidents with severity
3. Form an incident response channel
4. Communicate per the incident communication template
5. Focus on mitigation before root cause
6. Document the timeline during response
7. Schedule the postmortem within 48 hours of resolution

### Deployment
- Deployments happen [frequency/time]
- All production changes go through CI/CD; no manual production changes
- Feature flags for risky changes
- Canary or blue-green deployments for critical services
- Rollback procedure tested monthly

### Environments
| Environment | Purpose | Who Can Deploy | Data |
|-------------|---------|---------------|------|
| Local | Development | Every engineer | Synthetic |
| CI | Automated testing | CI system | Synthetic |
| Staging | Pre-production validation | Every engineer | Anonymized production |
| Production | Live traffic | On-call + TL | Real |

---

## 6. Career Growth

### Engineering Levels
| Level | Scope | Impact | Example |
|-------|-------|--------|---------|
| E1 | Task | Individual | Implements assigned capabilities |
| E2 | Feature | Team | Leads capability development |
| E3 | System | Team + cross-team | Owns service architecture |
| E4 | Domain | Organization | Sets technical direction for a domain |
| E5 | Organization | Company | Influences company-wide technology |

### Promotion Criteria
- Consistently performs at the next level for [timeframe]
- Demonstrates impact through concrete examples
- Receives strong peer feedback
- Completes growth plan milestones

### Learning and Development
- [budget] per year for conferences, courses, books
- Internal tech talks and workshops
- Pair programming and mentorship
- Quarterly hack days

---

## 7. Onboarding

### First Week
- [ ] Development environment set up; first commit merged
- [ ] Intro meetings with [list of roles/people]
- [ ] Read sections 1-3 of this handbook
- [ ] Onboarding buddy assigned: ______

### First 90 Days
| Milestone | By Day | Verified By |
|-----------|--------|-------------|
| Ships code independently | 30 | ______ |
| Completes on-call shadow | 60 | ______ |
| Owns a small project end to end | 90 | ______ |

---

## 8. How to Change This Handbook

Maintained by [owner]; changes go through:
1. Propose the change via PR to [handbook repo]
2. Discuss in #engineering or a team meeting
3. Merge after consensus from [team leads / all engineers]
4. Announce the change in #engineering
5. Update onboarding materials if affected

## Changelog

| Date | Change | Author |
|------|--------|--------|
| ______ | Initial version | ______ |
