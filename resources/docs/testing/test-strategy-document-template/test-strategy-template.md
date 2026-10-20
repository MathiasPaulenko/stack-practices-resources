# Test Strategy: `<Project Name>`

## 1. Objectives

- Verify that the product meets functional requirements
- Prevent regressions in critical user journeys
- Validate performance under expected and peak load
- Ensure security and data integrity
- Provide fast feedback to developers (under 10 minutes for PR pipeline)

## 2. Test Pyramid

| Layer | Proportion | Scope | Speed | Owner |
|-------|-----------|-------|-------|-------|
| Unit | 70% | Functions, classes, modules | < 30s | Developer |
| Integration | 20% | API + database + external services | < 5min | Developer |
| E2E | 7% | Full user journeys | < 15min | QA |
| Manual/Exploratory | 3% | Edge cases, usability, security | As needed | QA |

### Rationale

Unit tests are fast and isolate failures. Integration tests verify contracts between components. E2E tests validate real user flows but are slow and flaky. Manual testing covers what automation cannot: visual bugs, usability, and novel edge cases.

## 3. Test Scope

### In Scope

| Area | Coverage Target | Priority |
|------|----------------|----------|
| Authentication & authorization | 95% | Critical |
| Payment processing | 95% | Critical |
| Order management | 90% | High |
| User profile | 80% | Medium |
| Admin dashboard | 70% | Low |
| Marketing pages | 50% | Low |

### Out of Scope

- Third-party services (tested by their providers)
- Infrastructure provisioning (validated by Terraform tests)
- Visual regression (handled by design review)

## 4. Test Environments

| Environment | Purpose | Data | Refresh Cycle |
|-------------|---------|------|---------------|
| Local | Developer testing | Synthetic seed data | On demand |
| CI | Automated pipelines | Fresh per run | Per build |
| Staging | Pre-production validation | Anonymized prod snapshot | Weekly |
| Production | Smoke tests, synthetic monitoring | Real | N/A |

### Environment Parity Requirements

- Same database version and configuration
- Same OS and runtime versions
- Same environment variables (except secrets)
- Same third-party API versions (or mocks with matching behavior)

## 5. Tools and Frameworks

| Layer | Tool | Version | Notes |
|-------|------|---------|-------|
| Unit | Vitest / Jest | Latest | Coverage via v8 |
| Integration | Testcontainers + supertest | Latest | Real DB in Docker |
| E2E | Playwright | Latest | Cross-browser |
| Load | k6 | Latest | Scenario-based |
| Contract | Pact | Latest | Consumer-driven |
| Security | OWASP ZAP | Latest | DAST in CI |
| Coverage | c8 / istanbul | Latest | v8 instrumentation |

## 6. CI/CD Pipeline Gates

| Stage | Tests | Gate Condition | Timeout |
|-------|-------|----------------|---------|
| Pre-commit | Lint, type check | 0 errors | 30s |
| PR build | Unit + integration | 100% pass, coverage >= 80% | 10min |
| Merge to main | Full suite + contract | 100% pass, no new flaky tests | 20min |
| Nightly | E2E + load baseline | 95% pass, latency within 10% | 60min |
| Pre-release | Full load + soak + security | 100% pass, SLOs met | 120min |
| Post-release | Smoke tests + synthetic | 100% pass for 30min | 5min |

### Coverage Gates

| Metric | Threshold | Enforced By |
|--------|-----------|-------------|
| Line coverage | >= 80% | CI check |
| Branch coverage | >= 70% | CI check |
| Critical path coverage | >= 95% | Manual review |
| New code coverage | >= 90% | CI check (diff-based) |

## 7. Test Data Management

| Strategy | Use Case | Implementation |
|----------|----------|----------------|
| Factory functions | Most tests | `createUser()`, `createOrder()` helpers |
| Seed data | Integration tests | SQL scripts run before test suite |
| Fixtures | Stable reference data | JSON files in version control |
| Anonymized prod data | Staging only | ETL pipeline strips PII |
| Synthetic data | Load tests | Generated at scale, no PII |

### Data Cleanup

- Each test creates its own data and cleans up (teardown)
- Integration tests use transactions rolled back after each test
- Staging data refreshed weekly from anonymized production snapshot
- No test data in production — enforced by environment isolation

## 8. Flaky Test Policy

### Definition

A test is flaky if it passes and fails with the same code in > 5% of runs over 7 days.

### Process

1. Flaky test detected → tagged with `@flaky` in code
2. Notification sent to test owner in Slack
3. Owner has 3 business days to fix or quarantine
4. Quarantined tests moved to separate suite, not blocking CI
5. Quarantined tests must be fixed within 1 sprint or deleted
6. Flaky test rate tracked as a quality metric (target: < 1%)

## 9. Quality Metrics

| Metric | Target | Frequency | Owner |
|--------|--------|-----------|-------|
| Unit test coverage | >= 80% | Per build | Dev team |
| Integration test coverage | >= 70% | Per build | Dev team |
| Critical path coverage | >= 95% | Weekly | QA |
| Flaky test rate | < 1% | Daily | Dev team |
| Defect escape rate | < 5 per sprint | Per sprint | QA |
| Mean time to detect (MTTD) | < 1 hour | Per incident | SRE |
| Mean time to repair (MTTR) | < 4 hours | Per incident | Dev team |
| E2E pass rate | >= 95% | Daily | QA |

## 10. Risk-Based Testing

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Payment integration breaks | Low | Critical | Contract tests + integration tests + staging validation |
| Auth token expiry edge case | Medium | High | Unit tests for token refresh logic |
| Database migration failure | Medium | High | Migration tests in CI + dry run on staging |
| Third-party API downtime | Medium | Medium | Circuit breaker + fallback tests |
| Load spike on launch | High | Medium | Load tests + autoscaling validation |

## 11. Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| Developer | Write and maintain unit + integration tests |
| QA Engineer | Write and maintain E2E tests, exploratory testing |
| SRE | Maintain test environments, load test infrastructure |
| Tech Lead | Review test strategy, approve coverage exceptions |
| Product Manager | Define acceptance criteria for test coverage |

## 12. Review Cycle

- Test strategy reviewed quarterly
- Coverage targets adjusted based on defect data
- Tools evaluated annually or when pain points emerge
- Postmortem findings feed back into test strategy updates
