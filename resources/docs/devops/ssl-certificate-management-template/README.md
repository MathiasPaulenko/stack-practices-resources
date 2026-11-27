# SSL Certificate Management — Companion Kit

Companion material for the [SSL Certificate Management Template](https://stackpractices.com/docs/ssl-certificate-management-template/).

## Contents

| File | Description |
|------|-------------|
| `scripts/certbot-renew.sh` | Certbot renewal with deploy hook + Slack alert on failure |
| `scripts/certbot-wildcard.sh` | Wildcard issuance via DNS-01 (Cloudflare example) |
| `scripts/vault-pki.sh` | HashiCorp Vault PKI internal CA setup and issuance |
| `scripts/cert-expiry-check.sh` | Scan all Kubernetes TLS secrets, warn under N days |
| `scripts/ct-watch.sh` | Query crt.sh CT logs for unexpected certificates on your domains |
| `scripts/ocsp-refresh.sh` | Reload nginx to refresh stale OCSP stapling after renewal |
| `k8s/cert-manager.yaml` | ClusterIssuer (Let's Encrypt) + Certificate manifests |
| `sql/inventory-dashboard.sql` | Inventory query with CRITICAL/WARNING/INFO expiry buckets |
| `nginx/tls-hardening.conf` | TLS 1.2/1.3 only, cipher policy, HSTS preload |

## Usage

Review every script before running — paths (`/var/www/certbot`), container names (`nginx`), domains (`example.com`), and secrets paths are placeholders. Test on staging first.
