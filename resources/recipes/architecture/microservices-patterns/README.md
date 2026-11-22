# Microservices Resilience Patterns — companion examples

This folder contains runnable resilience-pattern examples for the
StackPractices recipe
[Microservices Resilience Patterns](https://stackpractices.com/recipes/microservices-patterns/).

## Files

| File | Description |
| --- | --- |
| `circuit_breaker.py` | Circuit breaker from scratch (stdlib): CLOSED → OPEN → HALF_OPEN states |
| `retry_backoff.mjs` | `p-retry` with exponential backoff and jitter around a payment call |
| `saga.ts` | Saga orchestration: steps with compensating actions run in reverse on failure |
| `package.json` | Node dependencies and scripts |
| `bulkhead.go` | Bulkhead with semaphores + `errgroup`: bounded concurrency per dependency |
| `go.mod` | Go module for the bulkhead example |
| `pom.xml` | Maven project for the Java example |
| `src/main/java/ResilientPaymentClient.java` | Resilience4j circuit breaker + retry + bulkhead + time limiter |
| `deployment.yaml` | Kubernetes Deployment with liveness/readiness/startup probes |
| `health_probes.ts` | Express endpoints backing the three probes |

## Running the examples

### Python (stdlib only)

```bash
python circuit_breaker.py
```

### Node.js / TypeScript

```bash
npm install
npm run retry    # needs a payments service endpoint
npm run saga     # wires SagaStep implementations
npm run probes   # Express health endpoints
```

### Go

```bash
go mod tidy
go run bulkhead.go
```

### Java

```bash
mvn compile
# ResilientPaymentClient wraps a payment call with a circuit breaker
# (50% failure threshold, 30s open), 3 retries, a 10-call bulkhead
# and a 3s time limiter.
```

### Kubernetes

```bash
kubectl apply -f deployment.yaml
```

## See also

- [Circuit Breaker Pattern](https://stackpractices.com/recipes/circuit-breaker-pattern-recipe/)
- [Retry and Backoff](https://stackpractices.com/recipes/retry-backoff/)
- [Saga Pattern](https://stackpractices.com/recipes/saga-pattern/)
