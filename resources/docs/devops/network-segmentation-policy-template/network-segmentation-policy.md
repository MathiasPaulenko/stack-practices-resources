# Network Segmentation Policy: `<Organization>`

| Field | Value |
|-------|-------|
| Owner | `<name / team>` |
| Approved by | `<CISO>` |
| Effective date | `YYYY-MM-DD` |
| Review cadence | `Quarterly` |
| Next review | `YYYY-MM-DD` |

## 1. Policy Statement

All production systems, sensitive data, and privileged access paths must reside in network segments separated from public, development, and guest networks. Traffic between segments is allowed only through approved paths, inspected by firewalls, and logged for monitoring.

## 2. Network Zones

| Zone | Trust Level | Purpose | Examples |
|------|-------------|---------|----------|
| Public | Untrusted | Internet-facing entry points | `<LB, CDN, WAF>` |
| DMZ | Low | Services that accept public traffic | `<web servers, gateways>` |
| Application | Medium | Internal business logic | `<app services>` |
| Data | High | Databases and persistent storage | `<postgres, caches>` |
| Management | High | Administrative interfaces | `<bastion, VPN>` |
| Development | Restricted | Engineering and test workloads | `<CI runners, dev VMs>` |
| Guest | Untrusted | Visitor or contractor access | `<guest Wi-Fi>` |

## 3. Allowed Traffic Matrix

| Source Zone | Destination Zone | Allowed | Protocol / Port | Justification | Control |
|-------------|------------------|---------|---------------|---------------|---------|
| `<zone>` | `<zone>` | `<Yes/No>` | `<proto port>` | `<why>` | `<enforcer>` |
| Development | Production | No | Any | Segregation of duties | Default deny |
| Guest | Management | No | Any | Protect admin paths | Default deny |

## 4. Segmentation Controls

| Control | Implementation | Owner | Frequency |
|---------|----------------|-------|-----------|
| Firewall rules | `<SG / firewall>` | Network team | Quarterly review |
| Route tables | `<subnet routing>` | Platform team | Per change |
| Network ACLs | `<stateless filtering>` | Security team | Quarterly review |
| Microsegmentation | `<workload policies>` | Platform team | Per change |
| DNS filtering | `<resolver policy>` | Security team | Continuous |
| VPN / Zero-trust | `<identity access>` | IAM team | Per change |

## 5. Exception Handling

| Exception ID | Description | Risk | Approved By | Expiration | Monitoring |
|--------------|-------------|------|-------------|------------|------------|
| EX-001 | `<desc>` | `<level>` | `<approver>` | `YYYY-MM-DD` | `<method>` |

## 6. Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| `<CISO>` | Owns policy and risk acceptance |
| `<network team>` | Implements firewall and routing rules |
| `<security team>` | Reviews exceptions and validates controls |
| `<platform team>` | Applies microsegmentation and cloud policies |
| `<compliance team>` | Maps policy to frameworks and audits evidence |
