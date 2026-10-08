# Post-Decommissioning Audit (30 days)

Run this audit one full billing cycle after the service stop date. The goal is
to catch whatever TTLs, scheduled jobs, and untagged resources hid during the
shutdown window.

## Infrastructure

- [ ] No cloud resources generating charges
- [ ] No active alerts referencing the service
- [ ] No obsolete dashboards in Grafana/Datadog
- [ ] No targets in Prometheus/CloudWatch

## Network and DNS

- [ ] DNS records deleted or redirected
- [ ] TLS certificates revoked or deleted
- [ ] Firewall/security group rules deleted
- [ ] Load balancers and target groups deleted

## Code and CI/CD

- [ ] Repository archived (not deleted)
- [ ] CI/CD pipelines disabled
- [ ] Webhooks removed
- [ ] CI environment variables deleted

## Data

- [ ] Backups archived to cheap storage
- [ ] Retention policy documented
- [ ] Access to archived data restricted and audited

## Documentation

- [ ] Tombstone created in wiki/documentation
- [ ] Service catalog updated
- [ ] Architecture diagrams updated
- [ ] Runbooks referencing the service updated
