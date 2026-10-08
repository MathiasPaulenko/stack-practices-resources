# Decommissioning Checklist: `<System / Service Name>`

> Service owner: ______ | Date: ______ | Approved by: ______
> Replacement system: ______ | Decommissioning target date: ______

## 1. Discovery

- [ ] List all upstream services that call this system
- [ ] List all downstream services this system calls
- [ ] List all external integrations (vendors, partners, webhooks)
- [ ] List all DNS entries, load balancers, and CDN configs pointing to this service
- [ ] List all SSL certificates tied to this service
- [ ] List all databases, caches, queues, and storage buckets owned by this service
- [ ] List all scheduled jobs, cron tasks, or background workers
- [ ] List all feature flags or configuration entries referencing this service

## 2. Data Handling

- [ ] Confirm data retention requirements (legal, compliance, business)
- [ ] Export and archive data that must be retained
- [ ] Verify archive location, encryption, and access controls
- [ ] Migrate active data to the replacement system
- [ ] Document the data archive location and retention schedule
- [ ] Confirm deletion of data that does not need to be retained

## 3. Dependency Removal

- [ ] Remove service from upstream load balancers and DNS
- [ ] Update upstream services to stop calling this system
- [ ] Remove service references from API gateways and service meshes
- [ ] Remove service from monitoring, alerting, and dashboards
- [ ] Remove service from CI/CD pipelines and deployment tools
- [ ] Remove service from secret managers and credential stores
- [ ] Remove service from backup schedules and disaster recovery plans

## 4. Shutdown

- [ ] Redirect traffic (if applicable) to replacement or sunset page
- [ ] Stop the service in staging / pre-production
- [ ] Monitor for errors or unexpected traffic for 24-48 hours
- [ ] Stop the service in production
- [ ] Monitor again for 24-48 hours
- [ ] Disable auto-restart or health-check recovery

## 5. Resource Cleanup

- [ ] Terminate compute instances, containers, or serverless functions
- [ ] Delete databases (after confirming archive and retention)
- [ ] Delete caches, queues, and topics
- [ ] Delete storage buckets and volumes
- [ ] Release static IPs and elastic network interfaces
- [ ] Delete load balancer listeners and target groups
- [ ] Delete DNS records (after TTL expires)
- [ ] Revoke or delete SSL certificates
- [ ] Delete IAM roles, policies, and service accounts

## 6. Documentation

- [ ] Update architecture diagrams to remove the service
- [ ] Update runbooks and operational documentation
- [ ] Update service catalog or ownership documents
- [ ] Write a brief postmortem or retrospective on the decommissioning
- [ ] Notify stakeholders that the service has been fully retired

## 7. Verification

- [ ] Confirm no billing charges for the service in the next billing cycle
- [ ] Confirm no alerts or errors reference the service
- [ ] Confirm no code repositories reference the service (excluding history)
- [ ] Confirm no new engineers are onboarding to the retired service
