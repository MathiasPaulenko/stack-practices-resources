# Sev-1 Timeline Example

A well-run Sev-1, minute by minute, on a SaaS platform whose API goes down. Notice the role separation: the IC coordinates, the Technical Lead investigates.

```text
Incident: API down, 100% of requests failing
Severity: Sev-1 (critical)
Start: 03:15 UTC
On-call: Ana (primary), Luis (secondary)

Response timeline:
  03:15 - Alert fires: APIErrorRate 100% on api-gateway
  03:16 - Ana receives page (PagerDuty)
  03:17 - Ana opens Slack #incident-sev1, declares Sev-1
  03:18 - Ana takes IC, assigns Luis as Technical Lead
  03:19 - Opens bridge (Zoom), invites team lead, DBA, infra
  03:21 - Luis verifies: 503 on all endpoints
  03:23 - Luis checks recent deploys:
         kubectl rollout history deploy/api-gateway
         -> Deploy v3.2 rolled out 12 min ago
  03:26 - Carlos (DBA) checks DB: connection pool 200/200
         with requests queuing -> saturation
  03:28 - Ana decides: rollback to v3.1 while Luis
         keeps investigating in parallel
  03:30 - Rollback executed: kubectl rollout undo
  03:33 - API restored, errors at 0%
  03:38 - Ana confirms stability for 5 min, resolves bridge
  03:42 - Final status update sent; postmortem scheduled (48h)
  03:45 - Scribe bot exports the channel timeline

Roles during the incident:
  | Role | Person | Responsibility |
  |------|--------|----------------|
  | Incident Commander | Ana | Coordinate, decide |
  | Technical Lead | Luis | Investigate, propose fixes |
  | Communications | Luis (until 03:40, then team lead) | Update stakeholders |
  | SME DB | Carlos (DBA) | Investigate database |
  | SME Infra | Pedro | Verify infrastructure |
  | Scribe | Bot | Timeline in Slack |

Communications:
  03:19 - #status: "Investigating Sev1 API down"
  03:26 - #status: "Identified: deploy v3.2 correlated with failure"
  03:28 - #status: "Executing rollback to v3.1"
  03:33 - #status: "API restored, monitoring"
  03:42 - #status: "Incident resolved. Postmortem in 48h"

Postmortem (48h):
  - Summary: API down 18 min due to defective deploy
  - Impact: 50K users affected, ~$15K revenue lost
  - Root cause: a migration in v3.2 introduced a query that
    scanned a large table without LIMIT. Under production
    load it held connections long enough to saturate the
    200-connection pool and queue all other requests.
  - 5 Whys:
    1. Why did it go down? Connection pool saturated
    2. Why saturated? A slow query held connections open
    3. Why not detected? Tests didn't cover production-scale load
    4. Why no load test? CI pipeline had no performance stage
    5. Why? Load testing was never prioritized for this service
  - Actions:
    1. Require LIMIT or pagination in queries (owner: team, 1 week)
    2. Add a k6 load test stage in CI (owner: platform, 2 weeks)
    3. Lower max pool connections per instance to 100 (owner: SRE, 3 days)
    4. Add pool saturation alert at 80% (owner: SRE, 3 days)
    5. Migration review checklist for risky queries (owner: team lead, 1 week)
```
