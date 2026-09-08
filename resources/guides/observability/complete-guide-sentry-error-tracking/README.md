# Sentry Error Tracking — Companion Examples

This directory contains companion code examples for the StackPractices guide
[Sentry: Error Tracking, Triage, and Resolution](https://stackpractices.com/guides/complete-guide-sentry-error-tracking/).

## Files

| File | Language | Description |
|------|----------|-------------|
| `sentry_config.py` | Python | Sentry SDK init, PII filtering, manual capture (Flask/Django) |
| `sentry_node.ts` | TypeScript | Sentry SDK init for Node.js (Express), custom spans |
| `SentryConfig.java` | Java | Sentry SDK config for Spring Boot |
| `release_tracking.sh` | Bash | Sentry release creation, commit association, source map upload |
| `alert_rules.yml` | YAML | Example alert rules (high error rate, new errors, perf regression) |
| `test_sentry_examples.py` | Python | Tests for the companion examples |

## Prerequisites

- Python 3.10+ with `sentry-sdk` and `pytest` installed
- Node.js 20+ with `@sentry/node` installed
- Java 17+ with `sentry-spring-boot-starter` installed
- `sentry-cli` installed globally (`npm install -g @sentry/cli`)

## Running the Tests

```bash
pip install pytest sentry-sdk
pytest test_sentry_examples.py -v
```

The tests verify the structure and syntax of the examples. The
`test_filter_sensitive_data_redacts_headers` test requires `sentry-sdk` to be
installed; the rest run without external dependencies.

## Usage

### Python (Flask/Django)

```python
from sentry_config import init_sentry
init_sentry()
```

### Node.js (Express)

```typescript
import { initSentry } from "./sentry_node";
initSentry();
```

### Java (Spring Boot)

Add `SentryConfig.java` to your Spring Boot application's configuration package.

### Release Tracking

```bash
SENTRY_AUTH_TOKEN=your_token ./release_tracking.sh
```
