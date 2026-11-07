# SOC 2 Evidence Map

Control → evidence → automation for the nine Common Criteria families. "Source of record" is where the artifact lives permanently; the evidence is what the auditor samples.

| CC | Control | Evidence | Source of record | Automation |
| --- | --- | --- | --- | --- |
| CC1 | Security policy acknowledged by all staff | Signed acknowledgment export | HRIS / policy tool | HRIS report on hire + annual re-ack |
| CC1 | Background checks for employees | Check completion records | HRIS | Flag missing checks >30 days after start |
| CC2 | Annual security training | Attendance log with dates | LMS / ticket system | Calendar-driven campaign, export roster |
| CC3 | Quarterly risk assessment | Updated risk register | Doc store | Scheduled review ticket with owner |
| CC4 | Quarterly access review | Review ticket + IAM diff | Ticket system | `access_review_diff.py` on IAM exports |
| CC5 | MFA enforced on all accounts | IdP policy export | Identity provider | IdP API compliance report |
| CC6 | Least-privilege roles on prod | Role assignment export | IAM | Scheduled export, alert on admin count delta |
| CC6 | Offboarding within 24 h | Ticket with revoke timestamps | HRIS + IdP | HR event triggers deprovisioning job |
| CC7 | Vulnerability scanning on every build | Scan results per artifact | CI artifacts | `trivy`/`snyk` in pipeline, findings → tickets |
| CC7 | Patch SLA met (crit ≤72h, high ≤7d) | Ticket resolution times | Issue tracker | SLA report query on vuln tickets |
| CC7 | Incident response drills | Postmortem + timeline | Doc store | Tabletop scheduled quarterly |
| CC8 | PR + approval on every change | Review trail on merged PRs | GitHub | `pr_approval_export.py` monthly archive |
| CC8 | Prod deploys require manual approval | Environment protection logs | CI/CD | `environment:` rule + audit log export |
| CC9 | Vendor due diligence per subservice org | Completed checklist + their SOC 2 | Doc store | `vendor-due-diligence-checklist.md` template |
| CC9 | Backups tested, not just taken | Restore-test logs with pass/fail | Job logs | Scheduled restore job writing results |
| A1 | Uptime monitored | Availability dashboard export | Monitoring | Status page history + alert history |
| C1 | Data encrypted at rest/in transit | KMS/TLS config exports | Cloud provider | `aws kms`/`gcloud kms` config snapshots |

## Notes

- Auditors sample, they don't exhaust: 25 items per control per period is typical. Every sampled item must be retrievable.
- The same artifact format every quarter beats a perfect format once. Consistency is what reads as "operating effectively."
- Anything that can't be exported from the source of record (screenshots of a UI you own) is weak evidence. Prefer API/CLI exports.
