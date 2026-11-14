# Expose Metrics with Micrometer and Prometheus — Companion Code

Runnable examples for the StackPractices recipe
[Expose Metrics with Micrometer and Prometheus](https://stackpractices.com/recipes/java-micrometer-prometheus/).

## What's inside

| File | What it shows |
| --- | --- |
| `OrderService.java` | `Counter` registered once in the constructor; `increment()` in the request path |
| `ConnectionPoolMonitor.java` | `Gauge` bound to a field — Micrometer weak-references the state object |
| `PaymentService.java` | `Timer` with `record()` and `publishPercentiles` |
| `DatabaseQueryExecutor.java` | `Timer.Sample` manual start/stop — the timer stays a field, no lookup per call |
| `OrderSizeTracker.java` | `DistributionSummary` for value distributions (items per order) |
| `UserService.java` | `@Counted` + `@Timed` annotations |
| `MetricsConfig.java` | `CountedAspect` bean — `TimedAspect` is auto-configured by Spring Boot |
| `CustomMetrics.java` | `MeterBinder` binding gauges to injected queue/cache objects |
| `StandaloneApp.java` | `PrometheusMeterRegistry` + `HTTPServer` builder (Prometheus client 1.x, Micrometer 1.12+) |
| `Models.java` | Shared record types used by the examples |
| `application.yml` | Endpoint exposure + common metric tags |
| `prometheus.yml` | Scrape config for the Actuator endpoint |

## Dependencies

Spring Boot 3.2+:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

`DatabaseQueryExecutor` also needs `spring-boot-starter-jdbc`.
`StandaloneApp` compiles against Micrometer 1.12+ — on the legacy Prometheus
simpleclient 0.x, use the `micrometer-registry-prometheus-simpleclient` module.

## Run

Drop the classes into a Spring Boot project, hit
`http://localhost:8080/actuator/prometheus`, and point the `prometheus.yml`
scrape config at it.
