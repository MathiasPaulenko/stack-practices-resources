# Change Risk Assessment Matrix

Use this matrix to classify the risk level of a change. The risk level decides
who must approve it.

## CRITICAL

- Changes to authentication or authorization
- Database schema changes affecting production data
- Network infrastructure changes (VPC, firewall, DNS)
- Changes during freeze periods (Black Friday, product launch)
- Changes affecting > 50% of user traffic

**Approval:** CAB + Security + Engineering Director

## HIGH

- Changes to production configuration
- API contract changes affecting external consumers
- Infrastructure scaling changes
- Database index additions/removals
- Changes affecting 10-50% of user traffic

**Approval:** CAB + Team Lead

## MEDIUM

- Feature flag toggles in production
- Non-breaking API additions
- Configuration parameter updates
- Dependency version bumps

**Approval:** Team Lead + Peer Review

## LOW

- CSS/styling changes
- Copy/text updates
- Documentation updates
- Non-production environment changes

**Approval:** Peer Review
