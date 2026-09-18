#!/bin/bash
# diagnose.sh - Automated diagnostic collector for on-call engineers
# Usage: ./diagnose.sh <service-name>

set -euo pipefail

SERVICE="${1:?Usage: $0 <service-name>}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
REPORT_DIR="/tmp/diagnostics-${SERVICE}-${TIMESTAMP}"

mkdir -p "$REPORT_DIR"

echo "=== Collecting diagnostics for $SERVICE at $TIMESTAMP ==="

# 1. Service status
echo "Checking service status..."
systemctl status "$SERVICE" 2>&1 | tee "$REPORT_DIR/service-status.txt" || true

# 2. Recent logs (last 100 lines)
echo "Collecting recent logs..."
journalctl -u "$SERVICE" --since "1 hour ago" --no-pager 2>&1 \
  | tail -100 > "$REPORT_DIR/recent-logs.txt" || true

# 3. Resource utilization
echo "Checking resource utilization..."
{
  echo "=== CPU ==="
  top -bn1 | head -20
  echo ""
  echo "=== Memory ==="
  free -h
  echo ""
  echo "=== Disk ==="
  df -h
  echo ""
  echo "=== Top processes by CPU ==="
  ps aux --sort=-%cpu | head -10
  echo ""
  echo "=== Top processes by Memory ==="
  ps aux --sort=-%mem | head -10
} > "$REPORT_DIR/resources.txt"

# 4. Network connectivity
echo "Checking network..."
{
  echo "=== Listening ports ==="
  ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null
  echo ""
  echo "=== Active connections ==="
  ss -tn state established 2>/dev/null | head -20
} > "$REPORT_DIR/network.txt"

# 5. Recent deployments
echo "Checking recent deployments..."
{
  echo "=== Docker containers ==="
  docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Docker not available"
  echo ""
  echo "=== Kubernetes pods ==="
  kubectl get pods -l app="$SERVICE" 2>/dev/null || echo "kubectl not available or no pods found"
} > "$REPORT_DIR/deployments.txt"

# 6. Health check
echo "Running health check..."
curl -sS -o "$REPORT_DIR/health-response.txt" -w "%{http_code}" \
  "http://localhost:8080/health" 2>&1 | tee "$REPORT_DIR/health-status.txt" || true

echo ""
echo "=== Diagnostics complete ==="
echo "Report saved to: $REPORT_DIR"
echo "Review files and attach to incident ticket."
