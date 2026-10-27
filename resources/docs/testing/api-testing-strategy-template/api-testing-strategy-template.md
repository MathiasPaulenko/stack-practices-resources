# API Testing Strategy: <API Name>

## Scope
- Endpoints covered: [list or link to OpenAPI spec]
- Consumers: [teams/apps calling this API]
- Out of scope: [what this document does not cover]

## Layer 1 — Contract Tests
- Tool: [Pact / Spring Cloud Contract / OpenAPI diff]
- Broker location: [URL]
- Verification gate: [CI step that fails the build]
- Owner: [team or person]

## Layer 2 — Integration Tests
- Tool: [supertest / pytest + httpx / JUnit]
- Environment: [Testcontainers / docker-compose / staging]
- Cases per endpoint: happy path + [list of failure modes]
- Owner: [team or person]

## Layer 3 — Load Tests
- Tool: [k6 / Gatling / JMeter]
- Scenarios: baseline [N RPS], spike [N RPS], soak [duration]
- Budgets: [p95 latency, error rate thresholds]
- Frequency: [weekly / pre-release]
- Owner: [team or person]

## Layer 4 — E2E
- Tool: [Cypress / Playwright]
- Journeys: [top 3 user flows]
- Frequency: [nightly]

## CI/CD Gates
| Stage | Runs | Budget |
|-------|------|--------|
| Pre-commit | lint + unit | [time] |
| PR build | integration + contract | [time] |
| Nightly | E2E + load baseline | [time] |
| Pre-release | full load + soak | [time] |

## Review Cadence
Last reviewed: [date] — Next review: [date] — Owner: [name]
