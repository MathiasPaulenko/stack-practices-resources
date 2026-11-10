# Status Page Message Templates

Short sentences, no hedging, always a next-update time. This is the full SEV 1 lifecycle; reuse it for SEV 2 with a 30-minute cadence.

## SEV 1: Initial Detection

```text
Status: Investigating
We are investigating an issue affecting [SERVICE/AFFECTED FEATURE].
Customers may experience [SYMPTOMS: e.g., login failures, slow responses].
We identified the issue at [TIME] and are actively working on a fix.
Next update in 15 minutes.
```

## SEV 1: Identified

```text
Status: Identified
We have identified the root cause: [PLAIN LANGUAGE DESCRIPTION].
A fix is being deployed and we expect service to be restored within [TIMEFRAME].
Next update in 15 minutes.
```

## SEV 1: Monitoring

```text
Status: Monitoring
A fix has been deployed and we're monitoring the service.
Preliminary indicators show improvement but we want to confirm stability.
Next update in 15 minutes.
```

## SEV 1: Resolved

```text
Status: Resolved
The issue has been resolved. Service is operating normally.
We will publish a postmortem within 72 hours.
Thank you for your patience.
```

## SEV 3 (single-post variant)

```text
Status: Investigating
We are aware of an issue affecting [SERVICE]. Impact is limited to [SCOPE].
A fix is in progress.

Status: Resolved
The issue has been resolved. Service is operating normally.
```
