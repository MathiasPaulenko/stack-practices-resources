#!/bin/bash
# Renew all Let's Encrypt certificates and reload nginx
set -euo pipefail

CERTBOT=/usr/bin/certbot
WEBROOT=/var/www/certbot
NGINX_CONTAINER=nginx

# Renew certificates
$CERTBOT renew --webroot --webroot-path $WEBROOT --quiet --deploy-hook "docker exec $NGINX_CONTAINER nginx -s reload"

# Check exit code
if [ $? -eq 0 ]; then
  echo "[$(date)] Certificate renewal successful" >> /var/log/certbot-renew.log
else
  echo "[$(date)] Certificate renewal FAILED" >> /var/log/certbot-renew.log
  # Send alert to Slack
  curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"SSL certificate renewal FAILED on $(hostname)"}' \
    $SLACK_WEBHOOK_URL
  exit 1
fi
