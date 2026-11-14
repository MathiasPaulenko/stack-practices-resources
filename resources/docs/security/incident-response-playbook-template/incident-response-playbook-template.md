# Incident Response Playbook: `<Incident Type>`

## Incident Metadata

| Field | Value |
|-------|-------|
| Incident ID | `INC-YYYY-MM-DD-###` |
| Severity | `P1 (Critical) / P2 (High) / P3 (Medium) / P4 (Low)` |
| Detected By | `@reporter` or `alert_system` |
| Detection Time | `YYYY-MM-DD HH:MM UTC` |
| Response Lead | `@incident-commander` |
| Status | `Open / Contained / Eradicated / Closed` |

## 1. Detection

### 1.1. Validate the Alert

- [ ] Confirm the alert is not a false positive
- [ ] Gather initial evidence (logs, screenshots, network captures)
- [ ] Document the first observed indicator of compromise (IOC)

### 1.2. Classify Severity

| Severity | Criteria | Response Time |
|----------|----------|---------------|
| P1 | Active data breach, ransomware, production down | < 15 minutes |
| P2 | Unauthorized admin access, malware detected | < 1 hour |
| P3 | Phishing attempt, low-privilege account compromise | < 4 hours |
| P4 | Vulnerability scan noise, policy violation | < 24 hours |

### 1.3. Assemble Response Team

- [ ] Assign Incident Commander (single decision-maker)
- [ ] Assign Technical Lead (forensics and remediation)
- [ ] Assign Communications Lead (internal/external updates)
- [ ] Page on-call security and infrastructure engineers

## 2. Containment

### 2.1. Short-Term Containment

- [ ] Isolate affected systems (disconnect network, disable accounts)
- [ ] Revoke compromised credentials (API keys, passwords, tokens)
- [ ] Block malicious IPs at firewall or WAF level
- [ ] Preserve evidence (snapshot disks, export logs)

### 2.2. Long-Term Containment

- [ ] Patch the vulnerability that enabled the incident
- [ ] Rotate all secrets in the affected scope
- [ ] Enable additional monitoring on related systems
- [ ] Restrict access to affected systems to response team only

## 3. Eradication

- [ ] Remove malware, backdoors, or unauthorized accounts
- [ ] Validate system integrity (checksums, known-good baselines)
- [ ] Rebuild compromised systems from known-good images
- [ ] Verify no persistence mechanisms remain (cron jobs, scheduled tasks)

## 4. Recovery

- [ ] Restore systems from clean backups (verify backup integrity first)
- [ ] Re-enable services with heightened monitoring
- [ ] Validate functionality with smoke tests
- [ ] Monitor for 24-72 hours for signs of re-infection
- [ ] Communicate all-clear to stakeholders

## 5. Lessons Learned

### 5.1. Timeline

| Time (UTC) | Action | Owner |
|------------|--------|-------|
| `T+0` | Alert fired | `@system` |
| `T+15m` | Incident Commander assigned | `@security` |
| `T+45m` | Containment complete | `@infra` |
| `T+3h` | Eradication complete | `@infra` |
| `T+6h` | Recovery complete | `@app-team` |

### 5.2. Root Cause

- What happened?
- Why did our controls fail?
- What was the blast radius (users, data, systems)?

### 5.3. Action Items

| ID | Action | Owner | Due Date |
|----|--------|-------|----------|
| A1 | Add WAF rule for attack pattern | `@security` | +3 days |
| A2 | Enable MFA for all admin accounts | `@identity` | +7 days |
| A3 | Improve log retention to 90 days | `@platform` | +14 days |
