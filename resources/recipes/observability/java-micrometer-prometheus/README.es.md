# Exponer Métricas con Micrometer y Prometheus — Código Companion

Ejemplos ejecutables de la receta de StackPractices
[Exponer Métricas con Micrometer y Prometheus](https://stackpractices.com/es/recipes/java-micrometer-prometheus/).

## Qué contiene

| Archivo | Qué muestra |
| --- | --- |
| `OrderService.java` | `Counter` registrado una vez en el constructor; `increment()` en el camino de la petición |
| `ConnectionPoolMonitor.java` | `Gauge` atado a un campo — Micrometer referencia débilmente el objeto de estado |
| `PaymentService.java` | `Timer` con `record()` y `publishPercentiles` |
| `DatabaseQueryExecutor.java` | `Timer.Sample` con arranque/parada manual — el timer queda como campo, sin búsqueda por llamada |
| `OrderSizeTracker.java` | `DistributionSummary` para distribuciones de valores (ítems por pedido) |
| `UserService.java` | Anotaciones `@Counted` + `@Timed` |
| `MetricsConfig.java` | Bean `CountedAspect` — `TimedAspect` lo autoconfigura Spring Boot |
| `CustomMetrics.java` | `MeterBinder` atando gauges a objetos inyectados de cola/caché |
| `StandaloneApp.java` | `PrometheusMeterRegistry` + builder `HTTPServer` (cliente Prometheus 1.x, Micrometer 1.12+) |
| `Models.java` | Records compartidos que usan los ejemplos |
| `application.yml` | Exposición del endpoint + etiquetas comunes |
| `prometheus.yml` | Config de scrape para el endpoint de Actuator |

## Dependencias

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

`DatabaseQueryExecutor` también necesita `spring-boot-starter-jdbc`.
`StandaloneApp` compila contra Micrometer 1.12+ — con el simpleclient
Prometheus 0.x legacy, usá el módulo `micrometer-registry-prometheus-simpleclient`.

## Ejecutar

Copiá las clases en un proyecto Spring Boot, abrí
`http://localhost:8080/actuator/prometheus` y apuntá el `prometheus.yml`
de scrape a ese endpoint.
