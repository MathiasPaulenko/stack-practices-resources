# Production Readiness Review: `<Service / Feature Name>`

> Reviewer: ______ | Date: ______ | Status: Pass / Conditional / Fail
> Service owner: ______ | Team: ______ | Release target: ______

---

## 1. Service Definition

- [ ] Service purpose is documented and understood by on-call engineers
- [ ] Service tier is defined (1 / 2 / 3) and matches operational requirements
- [ ] Service ownership document is complete and accessible
- [ ] Dependencies (upstream and downstream) are documented
- [ ] Data classification is defined (Public / Internal / Confidential / Restricted)

## 2. Architecture and Code Quality

- [ ] Architecture is reviewed and approved by a senior engineer or architect
- [ ] Code follows team standards (linting, formatting, test coverage)
- [ ] No known security vulnerabilities in dependencies (scanned within 30 days)
- [ ] Secrets are managed via secret manager, not hardcoded or in config files
- [ ] No single points of failure without documented mitigations

## 3. Testing

- [ ] Unit test coverage is above team minimum (usually 70-80%)
- [ ] Integration tests cover external dependencies and critical paths
- [ ] Load tests confirm the service handles expected peak traffic
- [ ] Chaos or failure injection tests verify graceful degradation
- [ ] End-to-end tests cover the full user journey where applicable

## 4. Observability

- [ ] Metrics are emitted for request rate, errors, and duration (RED)
- [ ] Logs are structured, correlated with trace IDs, and queryable
- [ ] Distributed tracing is configured for cross-service requests
- [ ] Dashboards exist for service health and key business metrics
- [ ] Alerting rules are configured with appropriate severity and thresholds
- [ ] On-call engineers can distinguish between symptoms and causes

## 5. Reliability and Resilience

- [ ] Health check endpoint exists and is used by load balancers
- [ ] Circuit breakers or bulkheads protect against cascading failures
- [ ] Timeouts and retries are configured for external calls
- [ ] Rate limiting is in place for public or partner-facing endpoints
- [ ] Database connections are pooled and bounded
- [ ] The service degrades gracefully when dependencies fail

## 6. Deployment and Release

- [ ] CI/CD pipeline exists and is green
- [ ] Deployments are automated; no manual production changes required
- [ ] Canary or staged rollout is configured for high-tier services
- [ ] Feature flags are available for risky or irreversible changes
- [ ] Database migrations are backward-compatible or have a tested rollback
- [ ] Rollback procedure is documented and tested within the last 30 days

## 7. Security

- [ ] Authentication and authorization are implemented correctly
- [ ] Input validation and sanitization protect against injection attacks
- [ ] Encryption in transit (TLS 1.2+) is enforced
- [ ] Sensitive data is encrypted at rest
- [ ] Security review is completed for auth, payment, or data-handling changes
- [ ] Penetration test or security scan results are reviewed and remediated

## 8. Data and State

- [ ] Database schema changes are reviewed for performance impact
- [ ] Backups are configured and tested (restore verified within 90 days)
- [ ] Data retention policies are documented and enforced
- [ ] GDPR / CCPA / compliance requirements are met for user data
- [ ] Migration scripts are idempotent and reversible where possible

## 9. Documentation

- [ ] README explains how to build, test, and run the service locally
- [ ] API documentation is current (OpenAPI / Swagger / equivalent)
- [ ] Runbooks exist for: deployment, rollback, common incidents, and escalation
- [ ] On-call handoff document is updated with recent changes and risks
- [ ] Architecture Decision Records (ADRs) cover major design choices

## 10. Operational Readiness

- [ ] On-call rotation is staffed and trained on this service
- [ ] Paging alerts reach the right people with useful context
- [ ] Escalation path is documented and contacts are verified
- [ ] Runbooks have been tested by someone who did not write the service
- [ ] Post-deployment verification steps are defined and automated where possible

---

## Review Notes

| Item | Finding | Risk | Mitigation / Action | Owner | Due Date |
|------|---------|------|---------------------|-------|----------|
| ______ | ______ | High / Medium / Low | ______ | ______ | ______ |

## Sign-Off

| Role | Name | Date | Signature (approve / block) |
|------|------|------|------------------------------|
| Engineering owner | ______ | ______ | ______ |
| Product owner | ______ | ______ | ______ |
| Security reviewer | ______ | ______ | ______ |
| SRE / Platform | ______ | ______ | ______ |
