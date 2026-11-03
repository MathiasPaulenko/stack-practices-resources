# Code Review Checklist

> Reviewer: ______ | Author: ______ | PR: ______ | Date: ______

## 1. Logic and Correctness
- [ ] The code does what the PR description claims it does
- [ ] Edge cases are handled (empty inputs, nulls, timeouts, failures)
- [ ] No off-by-one errors, race conditions, or infinite loops
- [ ] Error paths are explicit and do not swallow exceptions silently
- [ ] Business logic matches the spec or ticket requirements

## 2. Security
- [ ] No secrets, tokens, or credentials in code
- [ ] User inputs are validated and sanitized
- [ ] Authorization checks exist for protected operations
- [ ] No SQL injection, XSS, or command injection vulnerabilities
- [ ] Dependencies added are vetted and from trusted sources

## 3. Performance
- [ ] No N+1 queries or obvious algorithmic inefficiencies
- [ ] Large data sets are paginated or streamed
- [ ] No unnecessary network calls or blocking I/O in hot paths
- [ ] Caching is used appropriately where applicable
- [ ] Resource leaks (connections, file handles, memory) are prevented

## 4. Testing
- [ ] Unit tests cover the new or changed logic
- [ ] Integration tests cover external dependencies and boundaries
- [ ] Edge cases and failure paths are tested, not just happy paths
- [ ] Tests are deterministic and do not rely on timing or order
- [ ] Test names describe behavior, not implementation

## 5. Maintainability and Style
- [ ] Code is readable without needing to ask the author
- [ ] Variable and function names are descriptive and consistent
- [ ] No duplicated logic that could be extracted or reused
- [ ] Comments explain "why," not "what" (the code shows what)
- [ ] Complexity is appropriate; over-engineering is flagged

## 6. Documentation
- [ ] Public APIs have updated documentation or OpenAPI specs
- [ ] README or runbooks are updated if behavior changed
- [ ] Breaking changes are called out explicitly in the PR description
- [ ] Migration steps are documented if schema or config changed

## 7. Deployment and Operations
- [ ] Feature flags are used for risky or irreversible changes
- [ ] Monitoring and alerts are added or updated for new paths
- [ ] Rollback procedure is understood and tested
- [ ] Database migrations are backward-compatible or have a plan

---

## Review Notes

| Line / File | Issue | Severity | Action |
|-------------|-------|----------|--------|
| ______ | ______ | Nit / Suggestion / Blocker | ______ |

**Final verdict:** Approve / Request changes / Comment
**Merge readiness:** Ready / Needs work / Blocked

## Reviewer Confirmation

- [ ] I read every changed line
- [ ] I ran the tests locally
- [ ] I verified the PR description matches the changes
- [ ] I checked for breaking changes beyond the author's claims
