# Custom Health Checks with Spring Boot Actuator — Companion Code

All the code from the [Custom Health Checks with Spring Boot Actuator](https://stackpractices.com/recipes/java-actuator-health-checks/) recipe: every `HealthIndicator` variant plus the configuration that wires them into Kubernetes liveness/readiness probes.

## What's inside

| File | Purpose |
| --- | --- |
| `PaymentGatewayHealthIndicator.java` | External dependency check with `UP`/`DOWN` details (latency, provider, status code). |
| `DatabaseHealthIndicator.java` | Custom `SELECT 1` plus `pg_stat_activity` connection count via `JdbcTemplate`. |
| `RedisHealthIndicator.java` | Redis ping with latency — uses try-with-resources so `getConnection()` doesn't leak a connection per probe. |
| `ExternalApiHealthIndicator.java` | `java.net.http` check with separate connect (2s) and request (3s) timeouts. |
| `QueueDepthHealthIndicator.java` | "Degraded but alive" pattern: `UP` with a warning detail before the threshold, `DOWN` past it. |
| `AvailabilityService.java` | `ApplicationAvailability` + `AvailabilityChangeEvent` listeners; `markUnready()` drains the pod gracefully. |
| `ReactiveApiHealthIndicator.java` | `ReactiveHealthIndicator` returning `Mono<Health>` for Spring WebFlux. |
| `CustomStatusIndicator.java` | Registers a custom `Status("DEGRADED")` — note `@Component` registers the bean, there is no `@HealthIndicator` annotation. |
| `PaymentGatewayClient.java` / `PaymentGatewayStatus.java` / `MessageQueueService.java` | Stub types so the indicators compile in context. |
| `application.yml` | Endpoint exposure, `show-details`, `probes.enabled`, custom groups (`infrastructure`/`external`), readiness override, status HTTP mapping, disabling built-ins. |
| `kubernetes-deployment.yml` | `livenessProbe` and `readinessProbe` pointed at `/actuator/health/liveness` and `/actuator/health/readiness`. |

## Concepts covered

- **Liveness vs readiness** — liveness answers "is the JVM alive" (restart on failure), readiness answers "should I get traffic" (remove from rotation). Dependency checks belong in readiness, never liveness.
- **Timeouts are the check** — Kubernetes treats a probe timeout exactly like a DOWN, so a slow external check is a slow failure.
- **Groups over annotations** — `management.endpoint.health.group.*` is pure configuration; indicator names are bean names minus the `HealthIndicator` suffix.
- **DOWN is expensive** — report `UP` with warning details for degraded-but-working states; one vendor outage shouldn't restart your fleet.

## Dependencies

These classes target a Spring Boot 2.3+/3.x app with `spring-boot-starter-actuator`, `spring-boot-starter-web` (or `-webflux` for the reactive variant), `spring-boot-starter-data-redis`, and `spring-boot-starter-jdbc` on the classpath:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```
