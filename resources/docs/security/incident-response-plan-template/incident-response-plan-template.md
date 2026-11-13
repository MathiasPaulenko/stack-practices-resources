# Incident Response Plan — `<Organization Name>`

## Plan Overview

| Field | Value |
|-------|-------|
| Organization | Example Corp |
| Plan Version | 3.0 |
| Last Updated | 2026-07-05 |
| Plan Owner | CISO |
| Approved By | Executive Committee |
| Review Cycle | Quarterly |
| Next Review | 2026-10-05 |
| Compliance Frameworks | SOC 2, ISO 27001, GDPR, HIPAA |
| IR Team Size | 7 members |
| On-Call Rotation | 24/7, weekly rotation |

## 1. Incident Severity Classification

### Severity Levels

| Severity | Definition | Examples | Response Time | Escalation |
|----------|------------|----------|---------------|------------|
| SEV-0 (Critical) | Total service outage or active data breach | Production down, PII leaked, ransomware | 15 min | CEO, CISO, Legal, PR |
| SEV-1 (High) | Major service degradation or confirmed security breach | Partial outage, unauthorized access detected | 30 min | CISO, VP Engineering |
| SEV-2 (Medium) | Minor service degradation or suspected security issue | Slow response, suspicious activity flagged | 2 hours | Security Lead, On-call Eng |
| SEV-3 (Low) | Minor issue with no user impact | Single pod crash, config error | 4 hours | On-call Engineer |
| SEV-4 (Informational) | No impact, informational only | Security advisory, maintenance notification | Next business day | N/A |

### Severity Decision Matrix

| Impact \ Scope | Single User | Team | Department | Organization |
|----------------|-------------|------|------------|--------------|
| Data breach | SEV-1 | SEV-0 | SEV-0 | SEV-0 |
| Service outage | SEV-3 | SEV-2 | SEV-1 | SEV-0 |
| Performance degradation | SEV-4 | SEV-3 | SEV-2 | SEV-1 |
| Security alert (unconfirmed) | SEV-3 | SEV-2 | SEV-2 | SEV-1 |

## 2. Roles and Responsibilities

### Incident Response Team

| Role | Primary | Secondary | Responsibilities |
|------|---------|-----------|------------------|
| Incident Commander | CISO | VP Engineering | Coordinate response, make decisions, authorize actions |
| Technical Lead | Security Lead | Senior DevOps | Investigate, contain, eradicate threat |
| Communications Lead | PR Director | Marketing Director | Internal and external communications |
| Legal Counsel | General Counsel | External Legal | Legal obligations, regulatory notifications |
| HR Liaison | HR Director | HR Manager | Personnel issues, internal investigations |
| Scribe | Security Analyst | DevOps Engineer | Document timeline, decisions, actions |
| Executive Sponsor | CEO | COO | Business decisions, resource authorization |

### On-Call Schedule

| Rotation | Primary On-Call | Secondary On-Call | Escalation |
|----------|----------------|-------------------|------------|
| Week 1 | Security Lead A | DevOps Engineer A | CISO |
| Week 2 | Security Lead B | DevOps Engineer B | CISO |
| Week 3 | Security Lead A | DevOps Engineer A | VP Eng |
| Week 4 | Security Lead B | DevOps Engineer B | VP Eng |
| Holiday | Security Lead C | DevOps Engineer C | CISO + VP Eng |

### Contact Information

| Role | Name | Phone | Email | Slack |
|------|------|-------|-------|-------|
| Incident Commander | Jane Doe | +1-555-0101 | jane@example.com | @jane |
| Technical Lead | John Smith | +1-555-0102 | john@example.com | @john |
| Communications Lead | Mary Johnson | +1-555-0103 | mary@example.com | @mary |
| Legal Counsel | Robert Chen | +1-555-0104 | robert@example.com | @robert |
| HR Liaison | Sarah Williams | +1-555-0105 | sarah@example.com | @sarah |
| Executive Sponsor | CEO | +1-555-0100 | ceo@example.com | @ceo |

## 3. Incident Lifecycle

### Phase 1: Detection and Reporting

| Detection Source | Method | Alert Target | Response |
|------------------|--------|--------------|----------|
| SIEM alerts | Correlation rules | On-call Security | Page on-call |
| Monitoring alerts | Datadog/Prometheus | On-call DevOps | Page on-call |
| User reports | Help desk ticket | Security Team | Triage within 1 hour |
| External reports | Security researcher | Security Lead | Acknowledge within 24 hours |
| Threat intel | Feed correlation | SIEM auto-alert | Auto-page on SEV-0/1 |
| Compliance | Audit finding | Security Lead | Triage within 1 business day |

### Incident Report Template

```
Incident ID: INC-2026-001
Reported by: <name>
Date/Time detected: <YYYY-MM-DD HH:MM TZ>
Severity: <SEV-0/1/2/3/4>
Description: <brief description>
Affected systems: <list>
Affected users: <count or "unknown">
Data involved: <type, classification>
Current status: <investigating/contained/resolved>
Assigned to: <name>
```

### Phase 2: Triage and Assessment

| Step | Action | Responsible | Duration |
|------|--------|-------------|----------|
| 1 | Acknowledge incident | On-call | 5 min |
| 2 | Assign incident ID | On-call | 5 min |
| 3 | Assess severity | On-call + IC | 15 min |
| 4 | Assign roles | IC | 10 min |
| 5 | Create incident channel | Scribe | 5 min |
| 6 | Notify stakeholders | Communications Lead | 30 min |
| 7 | Start incident log | Scribe | Ongoing |
| 8 | Begin investigation | Technical Lead | Ongoing |

### Phase 3: Containment

#### Immediate Containment (SEV-0/SEV-1)

| Action | Command/Procedure | Duration | Approval |
|--------|-------------------|----------|----------|
| Isolate affected host | `kubectl cordon <node>; kubectl drain <node>` | 5 min | Tech Lead |
| Block malicious IP | Update WAF rules / firewall | 5 min | Tech Lead |
| Disable compromised account | `aws iam update-access-key --status Inactive` | 5 min | Tech Lead |
| Revoke active sessions | Force logout via IdP | 5 min | Tech Lead |
| Disable affected service | `kubectl scale deployment <name> --replicas=0` | 5 min | IC |
| Snapshot affected systems | Create disk snapshots for forensics | 15 min | Tech Lead |
| Preserve evidence | Capture logs, memory dumps | 30 min | Tech Lead |

#### Short-term Containment

| Action | Purpose | Duration |
|--------|---------|----------|
| Apply temporary firewall rules | Block attack vector | 30 min |
| Rotate compromised credentials | Prevent re-entry | 1 hour |
| Patch vulnerable software | Close attack vector | 2-4 hours |
| Deploy hotfix | Fix exploited bug | 2-6 hours |

#### Long-term Containment

| Action | Purpose | Duration |
|--------|---------|----------|
| Rebuild affected systems | Clean state | 4-24 hours |
| Update security rules | Prevent recurrence | 1-2 hours |
| Enhance monitoring | Detect similar attacks | 2-4 hours |
| Update detection rules | SIEM correlation | 1-2 hours |

### Phase 4: Eradication

| Step | Action | Verification |
|------|--------|--------------|
| 1 | Identify root cause | Forensic analysis |
| 2 | Remove malware/artifacts | Anti-malware scan, manual review |
| 3 | Close attack vector | Patch, config change, rule update |
| 4 | Validate eradication | Full system scan, penetration test |
| 5 | Document eradication steps | Incident log updated |

### Phase 5: Recovery

| Step | Action | Verification | Duration |
|------|--------|--------------|----------|
| 1 | Restore from clean backup | Backup integrity check | 1-4 hours |
| 2 | Rebuild affected systems | Configuration validation | 2-12 hours |
| 3 | Deploy patched version | Smoke tests pass | 1-2 hours |
| 4 | Gradual traffic restore | Health checks, monitoring | 30 min - 2 hours |
| 5 | Monitor for recurrence | Enhanced monitoring 72 hours | 72 hours |
| 6 | Validate with users | User acceptance testing | 1-4 hours |

### Phase 6: Post-Incident Review

| Step | Action | Responsible | Duration |
|------|--------|-------------|----------|
| 1 | Schedule review meeting | IC | Within 5 days |
| 2 | Collect all evidence | Scribe | Before meeting |
| 3 | Write incident timeline | Scribe | Before meeting |
| 4 | Conduct blameless review | All stakeholders | 1-2 hours |
| 5 | Identify root cause | Technical Lead | During review |
| 6 | Define corrective actions | Team | During review |
| 7 | Assign action items | IC | During review |
| 8 | Publish post-mortem | Scribe | Within 2 weeks |
| 9 | Track action items | IC | Until completion |

## 4. Communication Plan

### Internal Communications

| Audience | Channel | Timing | Content |
|----------|---------|--------|---------|
| IR Team | Slack incident channel | Real-time | Technical updates |
| Engineering | Slack #incidents | Every 30 min | Status updates |
| All employees | Email | Every 2 hours | High-level status |
| Executive team | Phone/Slack | Every 1 hour | Business impact |
| Board | Email via CEO | Within 24 hours | Summary for board |

### External Communications

| Audience | Channel | Timing | Content | Approval |
|----------|---------|--------|---------|----------|
| Customers | Status page | Within 30 min | Service impact | IC + Comms |
| Customers | Email | Within 24 hours | Detailed notification | IC + Legal |
| Regulatory bodies | Official notification | Per regulation | Required disclosure | Legal |
| Media | Press release | If publicly visible | Approved statement | CEO + Comms |
| Security researchers | Email | Within 48 hours | Acknowledgment | Security Lead |

### Communication Templates

#### Status Page Update (Initial)

```
[INVESTIGATING] We are investigating an issue affecting <service>.
Impact: <description of impact>.
Started: <timestamp>.
We will update within 30 minutes.
```

#### Status Page Update (Resolved)

```
[RESOLVED] The issue affecting <service> has been resolved.
Duration: <start> to <end>.
Root cause: <brief description>.
We will publish a post-incident review within 2 weeks.
```

#### Customer Notification Email

```
Subject: Security Incident Notification — <Date>

Dear <Customer>,

We are writing to inform you of a security incident that may have affected your data.
<Description of incident and impact>.
<What we have done in response>.
<What customers should do>.
We take this seriously and are taking the following steps: <action list>.
For questions, contact security@example.com.

Sincerely,
<Name>, <Title>
```

## 5. Regulatory Notification Requirements

| Regulation | Notification Deadline | Recipient | Trigger |
|------------|----------------------|-----------|---------|
| GDPR | 72 hours | Supervisory authority | Personal data breach |
| GDPR | Without undue delay | Data subjects | High risk to rights |
| CCPA | Without unreasonable delay | Affected consumers | Breach of PII |
| HIPAA | 60 days | HHS Secretary | PHI breach affecting 500+ |
| HIPAA | 60 days | Affected individuals | PHI breach |
| SOC 2 | Per agreement | Clients | Security incident |
| State laws | Varies (1-90 days) | State AG + residents | Per state law |

## 6. Incident Metrics

| Metric | Target | Measurement | Report |
|--------|--------|-------------|--------|
| Mean Time to Detect (MTTD) | < 15 min | Time from incident start to detection | Monthly |
| Mean Time to Respond (MTTR) | < 30 min | Time from detection to response start | Monthly |
| Mean Time to Contain (MTTC) | < 4 hours | Time from detection to containment | Monthly |
| Mean Time to Recover (MTTR) | < 24 hours | Time from containment to full recovery | Monthly |
| Incidents per quarter | Trending down | Count of incidents | Quarterly |
| Repeat incidents | < 5% | Incidents with same root cause | Quarterly |
| Post-incident reviews on time | 100% | Reviews within 5 days | Monthly |
| Action items completed | 100% | Corrective actions completed | Quarterly |
| Tabletop exercises | 4 per year | Exercises conducted | Annual |

## 7. Tabletop Exercise Plan

### Exercise Schedule

| Exercise | Scenario | Participants | Frequency |
|----------|----------|--------------|-----------|
| Exercise 1 | Ransomware attack | Full IR team | Quarterly |
| Exercise 2 | Data breach (PII leak) | IR team + Legal + PR | Quarterly |
| Exercise 3 | Insider threat | IR team + HR | Annually |
| Exercise 4 | DDoS attack | IR team + DevOps | Annually |
| Exercise 5 | Supply chain attack | Full IR team + Exec | Annually |

### Exercise Format

| Phase | Duration | Activity |
|-------|----------|----------|
| Setup | 15 min | Distribute scenario, assign roles |
| Inject 1 | 30 min | Initial incident report |
| Inject 2 | 30 min | Escalation (new information) |
| Inject 3 | 30 min | Complication (key person unavailable) |
| Hot wash | 30 min | Immediate feedback and lessons |
| Report | 1 week | Written findings and recommendations |
