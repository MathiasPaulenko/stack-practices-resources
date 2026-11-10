# Incident Communication: `<Incident Title>`

## 1. Incident Metadata

| Field | Value |
|-------|-------|
| Incident ID | `INC-YYYY-NNNN` |
| Service | `name` |
| Severity | `SEV 1 (Critical) / SEV 2 (Major) / SEV 3 (Minor)` |
| Start Time (UTC) | `YYYY-MM-DD HH:MM` |
| Detected By | `Monitoring / Customer report / Internal` |
| Incident Commander | `@name` |
| Communication Lead | `@name` — a separate person on SEV 1 |
| Status Page URL | `https://status.example.com` |

## 2. Audience Matrix

| Audience | Channel | First Notification | Owner |
|----------|---------|--------------------|-------|
| Engineering | Slack `#incidents` | Immediate | `@ic` |
| Support | Slack `#support-alerts` | Within 15 min | `@comms` |
| Executives | Email / Slack DM | Within 15 min | `@comms` |
| Customers | Status page, then email | Within 30 min | `@comms` |
| Enterprise accounts | Dedicated account channel | Within 30 min | `@account-team` |
| Legal / PR | Direct briefing | Before external disclosure if data is involved | `@comms` |

## 3. Message Templates

### 3.1. Initial Detection — Internal (Slack)

> **INCIDENT ALERT** — `<Service>` — `<SEV>`
>
> - **Status**: Investigating
> - **Symptoms**: `brief description`
> - **Impact**: `affected regions / capabilities / user segments`
> - **Started**: `time UTC`
> - **Actions**: Engineering is investigating. Updates every `15` minutes in `#incident-YYYY-MM-DD`.
> - **IC / Comms lead**: `@name` / `@name`

### 3.2. Initial Detection — Customer-Facing (Status Page)

> **Investigating — `<Service>` Issue**
>
> We are currently investigating reports of `symptom` affecting `service`. We will provide an update within 30 minutes or as soon as we have more information.
>
> **Affected**: `regions / capabilities`
> **Workaround**: `if any`
> **Next update by**: `time UTC`

### 3.3. Executive Summary (Email / Slack DM)

> **Incident Summary** — `<Service>` — `<SEV>`
>
> - **Impact**: `N customers / % of traffic / region`
> - **Revenue risk**: `High / Medium / Low / None`
> - **Root cause (preliminary)**: `one sentence, if known`
> - **ETA to resolution**: `only if confident`
> - **Actions taken**: `what's been done so far`
>
> I will send the next update within `timeframe`.

### 3.4. Update (On the Severity Cadence)

> **Update — `<Service>` Issue — `time UTC`**
>
> We have `identified the cause / implemented a mitigation / deployed a fix` for the `service` issue. `One sentence on what changed.`
>
> **Status**: Investigating / Identified / Monitoring
> **Next update by**: `time UTC`

### 3.5. Resolution

> **Resolved — `<Service>` Issue**
>
> `Service` is now fully operational. The issue was caused by `root cause in plain language`. All systems are stable and we're monitoring closely.
>
> **Duration**: `start–end time`
> **Impact**: `what users actually experienced`
> **Next steps**: We will publish a postmortem within `timeframe`.

### 3.6. Postmortem Notification

> **Postmortem — `<Service>` Incident on `Date`**
>
> We have completed our review of the incident on `date`. You can read the full postmortem here: `link`.
>
> - **Summary**: `one paragraph, no blame, no jargon`
> - **Impact**: `duration + affected users`
> - **Root cause**: `plain language`
> - **Fixes implemented**: `list`
> - **Prevention**: `what we're doing to avoid recurrence`

## 4. Severity Timing and Notification Matrix

| Severity | First Customer Update | Update Cadence | Internal Teams | Executives | Legal / PR |
|----------|----------------------|----------------|----------------|------------|------------|
| SEV 1 | 15 minutes | Every 15 minutes | Immediate | Within 15 min | If data involved |
| SEV 2 | 30 minutes | Every 30–60 minutes | Immediate | Within 30 min | If data involved |
| SEV 3 | 1 hour | Every 1–2 hours | Within 15 min | No | No |

Map the labels to your org's scale if you use P-levels: SEV 1 ≈ P1, SEV 2 ≈ P2, SEV 3 covers P3–P4.

## 5. Approval Checklist

- [ ] Message is factual; no resolution time promised unless the fix is already validating
- [ ] No internal jargon or technical detail that confuses customers
- [ ] Workaround is verified before publishing
- [ ] Legal / compliance reviewed if personal or regulated data is involved
- [ ] Status page is updated before any other channel
- [ ] Social media / PR is aligned if press may pick up the story
