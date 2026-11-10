# Incident Communication: `auth-service login failures (EU)`

## 1. Incident Metadata

| Field | Value |
|-------|-------|
| Incident ID | `INC-2026-0711` |
| Service | `auth-service` |
| Severity | `SEV 1 (Critical)` |
| Start Time (UTC) | `2026-07-11 10:58` |
| Detected By | `Monitoring (login error-rate alert)` |
| Incident Commander | `@on-call` |
| Communication Lead | `@comms` |
| Status Page URL | `https://status.example.com` |

## 2. Message Templates — Sent

### 3.1. Initial Detection — Internal (Slack, 11:00 UTC)

> **INCIDENT ALERT** — `auth-service` — `SEV 1`
>
> - **Status**: Investigating
> - **Symptoms**: HTTP 500s on login endpoint
> - **Impact**: ~15% of login attempts failing, EU region only
> - **Started**: 10:58 UTC
> - **Actions**: Engineering is investigating. Updates every 15 minutes in `#incident-2026-07-11`.
> - **IC / Comms lead**: `@on-call` / `@comms`

### 3.2. Initial Detection — Customer-Facing (Status Page, 11:12 UTC)

> **Investigating — Login Issues (EU)**
>
> We are currently investigating reports of login failures affecting users in the EU region. We will provide an update within 30 minutes or as soon as we have more information.
>
> **Affected**: EU region — login only
> **Workaround**: none
> **Next update by**: 11:30 UTC

### 3.3. Executive Summary (Email, 11:15 UTC)

> **Incident Summary** — `auth-service` — `SEV 1`
>
> - **Impact**: ~15% of EU login attempts failing since 10:58 UTC
> - **Revenue risk**: Medium (login, not checkout)
> - **Root cause (preliminary)**: config deploy changed JWT secret rotation
> - **ETA to resolution**: rollback in progress, ~15 min to confirm
> - **Actions taken**: bad config identified, rollback deployed at 11:08 UTC
>
> I will send the next update within 30 minutes.

### 3.4. Update — Customer-Facing (Status Page, 11:20 UTC)

> **Update — Login Issues (EU) — 11:20 UTC**
>
> We have identified the cause and deployed a fix for the login issue. Error rates are returning to normal.
>
> **Status**: Monitoring
> **Next update by**: 11:35 UTC

### 3.5. Resolution — Customer-Facing (Status Page, 11:35 UTC)

> **Resolved — Login Issues (EU)**
>
> `auth-service` is now fully operational. The issue was caused by a configuration error in our login service. All systems are stable and we're monitoring closely.
>
> **Duration**: 10:58–11:25 UTC (27 minutes)
> **Impact**: ~15% of EU login attempts failed during the window
> **Next steps**: We will publish a postmortem within 72 hours.

### 3.6. Postmortem Notification (Status Page + Email, 11:15 UTC + 2 days)

> **Postmortem — `auth-service` Incident on 2026-07-11**
>
> We have completed our review of the incident on 2026-07-11. You can read the full postmortem here: `link`.
>
> - **Summary**: A configuration deployment changed how login tokens were signed, rejecting valid sessions in the EU region.
> - **Impact**: 27 minutes; ~15% of EU login attempts failed.
> - **Root cause**: JWT secret rotation misapplied to one environment.
> - **Fixes implemented**: config rollback, secret rotation pinned per environment.
> - **Prevention**: config validation gate added to the deploy pipeline; rotation changes now require two-person review.
