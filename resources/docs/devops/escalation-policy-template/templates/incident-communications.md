# Incident Communication Templates

Copy-paste notices for each escalation stage. Keep placeholders in `<angle brackets>`.

## Initial Customer Notice (SEV 1)

```text
[INCIDENT] We are investigating an issue affecting <service>.
Impact: <description of user-facing impact>
Started: <timestamp UTC>
Status: Investigating
Next update: Within 15 minutes
```

## Initial Customer Notice (SEV 2)

```text
[INCIDENT] We are aware of degraded performance on <service>.
Impact: <description>
Started: <timestamp UTC>
Status: Investigating
Next update: Within 30 minutes
```

## Progress Update

```text
[UPDATE] <service> — <current status>.
What we know: <confirmed facts>
What we are doing: <current mitigation step>
Next update: Within <15|30> minutes
```

## Resolution Notice

```text
[RESOLVED] <service> is operating normally.
Duration: <total time>
Root cause: <brief summary>
Affected users: <approximate count or percentage>
Preventive action: <what we are doing to prevent recurrence>
```

## Internal Escalation Ping (Slack)

```text
:rotating_light: SEV <1|2> — <service> — paging L<2|3>
Summary: <one line>
Thread: <link to #incidents thread>
Bridge: <war room link>
IC: <@incident-commander>
```

## Executive Summary (for L4 awareness)

```text
SEV <level> on <service> since <HH:MM UTC>.
Impact: <users / revenue>
Status: <investigating | mitigating | monitoring>
ETA: <best estimate or "unknown">
Next update: <time>
IC: <name>
```
