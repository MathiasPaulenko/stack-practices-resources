# Logging Standards — [Organization Name]

Owner: [name/team] · Version: [x.y] · Last review: [date] · Next review: [date]

## 1. Log Levels

| Level | Use | Example |
|-------|-----|---------|
| DEBUG | Detailed diagnostic info, development only | `[example]` |
| INFO | Normal application events | `[example]` |
| WARN | Unexpected but recoverable | `[example]` |
| ERROR | Failures that affect operation — must alert | `[example]` |
| FATAL | Critical failures — must page on-call | `[example]` |

Rules:
- Production default level: `[INFO]`
- DEBUG enabled temporarily only via `[mechanism]`

## 2. Structured Log Format

All logs are emitted as JSON (UTF-8). Field naming convention: `snake_case`.

Required fields:

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 UTC | Event time |
| `level` | string | Log level |
| `service` | string | Service name |
| `environment` | string | `[dev/staging/production]` |
| `message` | string | Human-readable summary |
| `correlation_id` | string | Request trace ID |
| `span_id` | string | OpenTelemetry span ID |

Optional fields: `user_id`, `tenant_id`, `duration_ms`, `error_code`, `source_file`.

## 3. Required Event Categories

| Category | Events | Level |
|----------|--------|-------|
| Authentication | `[list]` | `[INFO/WARN]` |
| Authorization | `[list]` | `[level]` |
| Data changes | `[list]` | `[level]` |
| Errors | `[list]` | `[ERROR]` |
| Performance | `[list]` | `[level]` |
| Security | `[list]` | `[level]` |
| Operational | `[list]` | `[level]` |
| Business | `[list]` | `[level]` |

## 4. Sensitive Data and Redaction

| Data type | Logged | Rule |
|-----------|--------|------|
| Passwords | Never | — |
| Credit cards | Never | — |
| API keys / tokens | Never | — |
| Personal names | `[policy]` | `[mask/exclude]` |
| Emails | `[policy]` | `[rule]` |
| IP addresses | `[policy]` | `[rule]` |
| User IDs | Allowed | — |

Rules:
- Never log secrets or credentials.
- Personal data is allowlist-only.
- Redact/tokenize before the value reaches the log stream.

## 5. Retention and Sampling

| Log type | Retention | Sampling | Notes |
|----------|-----------|----------|-------|
| Application | `[30d]` | `[100%]` | |
| Security | `[1y]` | `[100%]` | |
| Audit | `[7y]` | `[100%]` | |
| Debug | `[7d]` | `[100%]` | only when enabled |
| High-volume | `[14d]` | `[1%]` | cost control |

## 6. Aggregation and Transport

| Requirement | Rule |
|-------------|------|
| Transport | `[platform + backpressure behavior]` |
| Buffering | `[local buffer policy]` |
| Encoding | UTF-8 JSON |
| Alerting | ERROR/FATAL routed to `[alerting system]` |

## Changelog

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | `[date]` | Initial version | `[name]` |
