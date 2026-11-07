# Data Breach Response Playbook

> Playbook owner: ______ | Last updated: ______
> Incident response team: ______ | Legal contact: ______

## Phase 1: Detection and Assessment (0-2 hours)

### Immediate actions

- [ ] Confirm the breach is real (rule out false positive)
- [ ] Document the initial indicator: time, source, type of alert
- [ ] Classify data involved: PII, PHI, financial, credentials, intellectual property, other
- [ ] Estimate number of records or users affected
- [ ] Assign incident commander and roles
- [ ] Open a secure, restricted communication channel (not the general incident channel)

### Decision: does this trigger notification requirements?

| Jurisdiction | Trigger | Timeline | Notes |
|-------------|---------|----------|-------|
| GDPR | Personal data compromised | 72 hours to supervisory authority | ______ |
| CCPA / CPRA | Personal info accessed without authorization | Without unreasonable delay | ______ |
| State laws (US) | Varies by state | Varies | ______ |
| Contractual | Defined in DPA or MSA | Defined in agreement | ______ |

## Phase 2: Containment (2-24 hours)

### Technical containment

- [ ] Isolate compromised systems (do not power off — preserve volatile memory)
- [ ] Revoke compromised credentials and sessions
- [ ] Block unauthorized IPs or accounts at firewall / WAF level
- [ ] Disable compromised API keys or service accounts
- [ ] Rotate all secrets that may have been exposed
- [ ] Preserve logs, snapshots, and disk images before cleanup

### Administrative containment

- [ ] Restrict access to incident details to need-to-know personnel
- [ ] Pause non-essential deployments or changes
- [ ] Brief executive leadership on scope and response status

## Phase 3: Evidence Preservation and Investigation (24-72 hours)

- [ ] Engage forensics team (internal or external)
- [ ] Create forensic images of affected systems
- [ ] Collect and preserve logs: application, database, network, access, audit
- [ ] Document chain of custody for all evidence
- [ ] Build timeline of attacker activity: initial access, lateral movement, data access, exfiltration
- [ ] Identify root cause: vulnerability, misconfiguration, credential theft, insider threat, third-party compromise

## Phase 4: Notification (per legal timeline)

### Internal notification

- [ ] Board / executive leadership
- [ ] Legal counsel
- [ ] Insurance provider (cyber liability)
- [ ] HR (if insider threat suspected)

### External notification

- [ ] Regulatory bodies (per applicable law)
- [ ] Affected customers / users
- [ ] Partners or vendors if their data was involved
- [ ] Law enforcement (if required or advisable)

### Notification content checklist

- [ ] What happened
- [ ] What data was involved
- [ ] What steps were taken to contain the breach
- [ ] What steps affected individuals should take
- [ ] Contact information for questions
- [ ] What the organization is doing to prevent recurrence

## Phase 5: Remediation and Recovery (1-4 weeks)

- [ ] Patch or fix the root cause vulnerability
- [ ] Remove attacker persistence mechanisms (backdoors, accounts, scheduled tasks)
- [ ] Rebuild compromised systems from known-good sources if integrity is uncertain
- [ ] Re-enable systems with enhanced monitoring
- [ ] Verify no unauthorized access persists
- [ ] Conduct a security review of affected systems
- [ ] Update security controls: MFA, segmentation, logging, alerting

## Phase 6: Post-Incident (2-4 weeks)

- [ ] Conduct a blameless postmortem
- [ ] Track and complete all remediation action items
- [ ] Review and update this playbook based on lessons learned
- [ ] Review data inventory and access controls
- [ ] Update risk assessment and insurance coverage if needed
- [ ] Publish a transparent summary to affected parties (as appropriate)

## Roles and Responsibilities

| Role | Responsibilities | Primary | Backup |
|------|------------------|---------|--------|
| Incident Commander | Primary coordination, decision authority, stakeholder updates | ______ | ______ |
| Technical Lead | Containment, forensics, remediation | ______ | ______ |
| Legal Counsel | Notification requirements, regulatory compliance, privilege | ______ | ______ |
| Communications Lead | Customer, media, and internal messaging | ______ | ______ |
| HR Representative | Insider threat, employee impact | ______ | ______ |

## Contact List

| Party | Contact | Method | Notes |
|-------|---------|--------|-------|
| Legal counsel | ______ | ______ | ______ |
| Cyber insurance | ______ | ______ | ______ |
| Forensics firm | ______ | ______ | ______ |
| Law enforcement | ______ | ______ | ______ |
| Regulatory body | ______ | ______ | ______ |
