# API Lifecycle Management: `<API Name>`

## 1. API Metadata

| Field | Value |
|-------|-------|
| API Name | `name` |
| Current Version | `v2.3` |
| Base URL | `https://api.example.com/v2` |
| Owner Team | `@platform-team` |
| Consumers | Internal: 3, External: 12 |
| Lifecycle State | Published / Deprecated / Sunset / Retired |

## 2. Deprecation Checklist

### 2.1. Decision & Communication

- [ ] Document the reason for deprecation (security, performance, maintainability)
- [ ] Identify all consumers using the deprecated endpoint/version
- [ ] Set a deprecation date (minimum 6 months for external APIs, 3 months for internal)
- [ ] Publish deprecation notice in:
  - [ ] API documentation (changelog)
  - [ ] Developer portal / status page
  - [ ] Direct email to registered consumers
  - [ ] Response headers (`Deprecation`, `Sunset`, `Link` relations)

### 2.2. Migration Path

- [ ] Provide a migration guide with before/after examples
- [ ] Offer a sandbox environment for testing the new version
- [ ] Schedule office hours or Q&A sessions for consumer teams
- [ ] Create a compatibility shim if the migration is complex

### 2.3. Monitoring

- [ ] Track traffic to the deprecated endpoint daily
- [ ] Alert when usage drops below threshold (ready for shutdown)
- [ ] Maintain a dashboard of consumer migration progress
- [ ] Log which consumers still call the deprecated version, not just how many

## 3. Versioning Checklist

### 3.1. Version Selection

- [ ] Determine if the change is backward-compatible (patch/minor) or breaking (major)
- [ ] Follow semantic versioning: `MAJOR.MINOR.PATCH`
- [ ] Update URL path (`/v3/`) or use header-based versioning (`Accept: application/vnd.api.v3+json`)

### 3.2. Release

- [ ] Deploy the new version alongside the old version
- [ ] Update documentation with new request/response examples
- [ ] Run contract tests against the new version
- [ ] Verify backward compatibility for non-breaking changes

### 3.3. Post-Release

- [ ] Monitor error rates and latency for the new version
- [ ] Collect feedback from early adopters
- [ ] Update SDKs and client libraries
- [ ] Record adoption per consumer to seed the next deprecation plan

## 4. Sunset Checklist

### 4.1. Pre-Shutdown

- [ ] Confirm zero traffic to the deprecated endpoint for 7 consecutive days
- [ ] Verify all known consumers have migrated (contact stragglers individually)
- [ ] Announce the final shutdown date (30 days notice)

### 4.2. Shutdown

- [ ] Disable the endpoint (return `410 Gone` or `404 Not Found`)
- [ ] Remove deprecated code and tests
- [ ] Update infrastructure (load balancer rules, DNS)
- [ ] Archive documentation with a redirect to the new version

### 4.3. Post-Shutdown

- [ ] Monitor for unexpected 404s from unknown consumers
- [ ] Document lessons learned
- [ ] Update API lifecycle timeline
