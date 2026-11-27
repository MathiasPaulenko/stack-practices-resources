# certbot wildcard issuance with Cloudflare DNS
certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials ~/.secrets/cloudflare.ini \
  -d "*.example.com" \
  -d "example.com" \
  --non-interactive \
  --agree-tos \
  --email platform-team@company.com
