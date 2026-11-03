# Game Day: <Date>

## Participants
- Facilitator: <name>
- Observers: <names>
- On-call engineer: <name>

## Scope
- Target service: payment-service
- Environment: staging
- Blast radius: 10% of traffic

## Experiments
1. Kill primary database pod - expect failover < 30s
2. Inject 500ms latency to payment gateway - expect p99 < 2s
3. Drop 20% of packets to Redis - expect cache miss rate increase only

## Abort Criteria
- Error rate > 1% for > 2 minutes
- p99 latency > 5s
- Any data corruption detected

## Rollback Plan
- `kubectl rollout undo deployment/payment-service`
- `toxiproxy-cli toxic delete --all`
- Page on-call engineer
