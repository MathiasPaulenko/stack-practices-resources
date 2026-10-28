#!/bin/bash
# Switch traffic from blue to green via Nginx upstream, with instant rollback.

BLUE_IP="10.0.1.10"
GREEN_IP="10.0.1.11"
NGINX_CONF="/etc/nginx/sites-enabled/app"

sed -i "s/server $BLUE_IP:8080/server $GREEN_IP:8080/" "$NGINX_CONF"
nginx -s reload

if ! curl -sf "http://$GREEN_IP:8080/health"; then
  sed -i "s/server $GREEN_IP:8080/server $BLUE_IP:8080/" "$NGINX_CONF"
  nginx -s reload
  echo "Rollback complete"
  exit 1
fi
