#!/usr/bin/env bash
# cross-region-failover.sh — controlled failover drill for Aurora Global + Route 53
# Prereqs: aws cli v2, jq, curl, dig, GNU date (gdate on macOS).
# Usage: ./failover.sh --dry-run   then   ./failover.sh
set -euo pipefail

PRIMARY_REGION="${PRIMARY_REGION:-us-east-1}"
SECONDARY_REGION="${SECONDARY_REGION:-eu-west-1}"
GLOBAL_CLUSTER_ID="${GLOBAL_CLUSTER_ID:?Set GLOBAL_CLUSTER_ID to the Aurora global cluster name}"
SECONDARY_CLUSTER_ARN="${SECONDARY_CLUSTER_ARN:?Set SECONDARY_CLUSTER_ARN for the cluster being promoted}"
SECONDARY_CLUSTER_ID="${SECONDARY_CLUSTER_ID:?Set SECONDARY_CLUSTER_ID (cluster resource name for lag metrics)}"
HOSTED_ZONE_ID="${HOSTED_ZONE_ID:?Set HOSTED_ZONE_ID for the Route 53 zone}"
DNS_RECORD="${DNS_RECORD:?Set DNS_RECORD, e.g. api.example.com}"
SECONDARY_CNAME="${SECONDARY_CNAME:?Set SECONDARY_CNAME, the regional endpoint to point at}"
SECONDARY_HEALTH_URL="${SECONDARY_HEALTH_URL:?Set SECONDARY_HEALTH_URL, e.g. https://eu-west-1.api.internal/health}"
ASG_NAME="${ASG_NAME:?Set ASG_NAME for the secondary Auto Scaling group}"
ASG_DESIRED="${ASG_DESIRED:-10}"
RPO_MAX_MS="${RPO_MAX_MS:-300000}"   # 5 minutes in milliseconds
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    *) echo "Unknown flag: $arg" >&2; exit 2 ;;
  esac
done

log() { printf '%s %s\n' "$(date -u +%H:%M:%SZ)" "$*"; }
run() { if [ "$DRY_RUN" -eq 1 ]; then log "DRY-RUN: $*"; else "$@"; fi; }

if [ "$DRY_RUN" -eq 0 ]; then
  read -r -p "Type FAILOVER to promote $SECONDARY_REGION: " answer
  [ "$answer" = "FAILOVER" ] || { log "Aborted by operator."; exit 1; }
fi

START=$(date +%s)

# 1. Secondary health
log "[1/6] Checking secondary region health"
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$SECONDARY_HEALTH_URL" || true)
[ "$code" = "200" ] || { log "FAIL: secondary unhealthy (HTTP ${code:-none})"; exit 1; }
log "  secondary healthy"

# 2. Replication lag within RPO (AuroraGlobalDBRPOLag, milliseconds)
log "[2/6] Reading replication lag from CloudWatch"
LAG_MS=$(aws cloudwatch get-metric-statistics \
  --region "$PRIMARY_REGION" --namespace AWS/RDS \
  --metric-name AuroraGlobalDBRPOLag \
  --dimensions Name=DBClusterIdentifier,Value="$SECONDARY_CLUSTER_ID" \
  --start-time "$(date -u -d '2 minutes ago' +%FT%TZ)" \
  --end-time "$(date -u +%FT%TZ)" --period 60 --statistics Maximum \
  --query 'Datapoints[-1].Maximum' --output text)
[ "$LAG_MS" != "None" ] || { log "FAIL: no lag datapoints"; exit 1; }
log "  lag = ${LAG_MS} ms (budget ${RPO_MAX_MS} ms)"
awk -v lag="$LAG_MS" -v max="$RPO_MAX_MS" 'BEGIN{exit !(lag <= max)}' \
  || { log "FAIL: lag exceeds RPO budget"; exit 1; }

# 3. Promote secondary database (planned switchover; use failover-global-cluster
#    for unplanned recovery, promote-read-replica-db-cluster for non-global replicas)
log "[3/6] Switching over global cluster to secondary"
run aws rds switchover-global-cluster \
  --global-cluster-identifier "$GLOBAL_CLUSTER_ID" \
  --target-db-cluster-identifier "$SECONDARY_CLUSTER_ARN"
if [ "$DRY_RUN" -eq 0 ]; then
  aws rds wait db-cluster-available \
    --region "$SECONDARY_REGION" \
    --db-cluster-identifier "$SECONDARY_CLUSTER_ARN"
fi
log "  secondary cluster promoted"

# 4. Scale secondary compute
log "[4/6] Scaling secondary ASG to $ASG_DESIRED"
run aws autoscaling set-desired-capacity \
  --region "$SECONDARY_REGION" \
  --auto-scaling-group-name "$ASG_NAME" \
  --desired-capacity "$ASG_DESIRED"

# 5. Shift DNS
log "[5/6] Updating Route 53 record $DNS_RECORD"
CHANGE_BATCH=$(jq -n --arg n "$DNS_RECORD" --arg v "$SECONDARY_CNAME" '{
  Changes: [{Action: "UPSERT", ResourceRecordSet: {
    Name: $n, Type: "CNAME", TTL: 60,
    ResourceRecords: [{Value: $v}]}}]}')
run aws route53 change-resource-record-sets \
  --hosted-zone-id "$HOSTED_ZONE_ID" --change-batch "$CHANGE_BATCH"

# 6. Verify resolution and traffic
log "[6/6] Verifying DNS and traffic"
for i in 1 2 3 4 5 6; do
  resolved=$(dig +short "$DNS_RECORD" @1.1.1.1 | tail -1)
  [ "$resolved" = "$SECONDARY_CNAME" ] && break
  log "  attempt $i: got '${resolved:-nothing}', waiting 10s"
  sleep 10
done
[ "$resolved" = "$SECONDARY_CNAME" ] || { log "FAIL: DNS did not converge"; exit 1; }

code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "https://$DNS_RECORD/health" || true)
log "  public health: HTTP ${code:-none}"
log "=== Done in $(( $(date +%s) - START ))s — soak for 30 min before failback ==="
