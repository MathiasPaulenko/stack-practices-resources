# Network Security Inventory: `<Environment>`

> Blank copy-paste template from https://stackpractices.com/docs/network-security-template/

## 1. Scope

| Field | Value |
|-------|-------|
| Environment | `prod / staging / dev` |
| Cloud Provider | `AWS / GCP / Azure / On-prem` |
| Network CIDR | `10.0.0.0/16` |
| Last Reviewed | `YYYY-MM-DD` |
| Reviewer | `@security-team` |

## 2. VPC / Network Segmentation

| Segment | CIDR | Purpose | Internet Access | Peering |
|---------|------|---------|-----------------|---------|
| Public subnet | `10.0.1.0/24` | Load balancers, bastion | Yes (egress only) | None |
| Application subnet | `10.0.2.0/24` | Microservices | No | Peered to shared services |
| Database subnet | `10.0.3.0/24` | PostgreSQL, Redis | No | Peered to shared services |
| Management subnet | `10.0.4.0/24` | CI/CD runners, monitoring | Yes (NAT) | None |
| Shared services | `10.1.0.0/24` | SSO, logging, secrets | No | Peered to all VPCs |

## 3. Firewall / Security Group Rules

### 3.1. Inbound Rules

| Source | Protocol | Port | Destination | Justification | Last Reviewed |
|--------|----------|------|-------------|---------------|---------------|
| `0.0.0.0/0` | TCP | 443 | Public ALB | Public HTTPS | `YYYY-MM-DD` |
| `10.0.2.0/24` | TCP | 5432 | Database subnet | Application → DB | `YYYY-MM-DD` |
| `10.0.4.0/24` | TCP | 22 | Bastion host | Admin access | `YYYY-MM-DD` |
| `VPN CIDR` | TCP | 3389 | Windows jump host | Admin access | `YYYY-MM-DD` |

### 3.2. Outbound Rules

| Destination | Protocol | Port | Source | Justification | Last Reviewed |
|-------------|----------|------|--------|---------------|---------------|
| `0.0.0.0/0` | TCP | 443 | All subnets | Software updates, APIs | `YYYY-MM-DD` |
| `0.0.0.0/0` | TCP | 53 | All subnets | DNS resolution | `YYYY-MM-DD` |
| `0.0.0.0/0` | UDP | 53 | All subnets | DNS resolution | `YYYY-MM-DD` |
| `SaaS IP range` | TCP | 443 | Application subnet | Third-party API | `YYYY-MM-DD` |

## 4. DNS Configuration

| Record | Type | Value | TTL | Purpose | Secured |
|--------|------|-------|-----|---------|---------|
| `api.example.com` | A | ALB IP | 60s | Public API | DNSSEC enabled |
| `internal.example.com` | A | Private IP | 300s | Internal services | Private zone only |
| `cdn.example.com` | CNAME | `cdn.provider.com` | 300s | Asset delivery | HTTPS enforced |

## 5. Network Access Controls

| Control | Implementation | Scope | Status |
|---------|----------------|-------|--------|
| DDoS protection | AWS Shield / Cloud Armor / Azure DDoS | Public endpoints | Active |
| WAF | AWS WAF / Cloudflare / ModSecurity | Public endpoints | Active |
| Intrusion detection | Suricata / GuardDuty / Azure Sentinel | VPC flow logs | Active |
| VPN / Zero Trust | WireGuard / Zscaler / BeyondCorp | All admin access | Active |
| Private endpoints | VPC endpoints / PrivateLink / Private Link | AWS / Azure services | Active |

## 6. Change Log

| Date | Change | Requester | Approved By | Ticket |
|------|--------|-----------|-------------|--------|
| `YYYY-MM-DD` | Opened port 5432 for new analytics service | `data-team` | `security-team` | `SEC-123` |
| `YYYY-MM-DD` | Removed SSH from public subnet | `sre-team` | `security-team` | `SEC-124` |
