# Setup SSL Certificates with Let's Encrypt — Companion Resources

Companion files for [Setup SSL Certificates with Let's Encrypt](https://stackpractices.com/recipes/setup-ssl-certificates/) on StackPractices.

## Files

| File | What it demonstrates |
|------|----------------------|
| `docker-compose.yml` | nginx + certbot sidecar with a renewal loop (`certbot renew` every 12h) |
| `nginx.conf` | HTTP→HTTPS redirect with the ACME `/.well-known/acme-challenge/` path mapped to the shared volume |
| `cloudflare.ini.example` | Credentials template for `certbot-dns-cloudflare` (wildcard certs via DNS-01) |
| `cert-manager.yaml` | `ClusterIssuer` + `Ingress` for automatic certs on Kubernetes |

## How to use

Docker setup (replace `example.com` with your real domain):

```bash
mkdir -p certbot/conf certbot/www certbot/log
docker compose up -d
```

Issue the first certificate:

```bash
docker compose run --rm certbot certonly --webroot \
  -w /var/www/certbot -d example.com -d www.example.com
```

For Kubernetes, `kubectl apply -f cert-manager.yaml` after installing cert-manager.

The `cloudflare.ini` credentials file must be `chmod 600` — it holds a plain-text API token.
