# Health Checks Personalizados con Spring Boot Actuator — Código Complementario

Todo el código de la receta [Health Checks Personalizados con Spring Boot Actuator](https://stackpractices.com/es/recipes/java-actuator-health-checks/): cada variante de `HealthIndicator` más la configuración que las conecta a los probes de liveness/readiness de Kubernetes.

## Qué contiene

| Archivo | Propósito |
| --- | --- |
| `PaymentGatewayHealthIndicator.java` | Verificación de dependencia externa con detalles `UP`/`DOWN` (latencia, proveedor, código de estado). |
| `DatabaseHealthIndicator.java` | `SELECT 1` personalizado más conteo de conexiones de `pg_stat_activity` vía `JdbcTemplate`. |
| `RedisHealthIndicator.java` | Ping a Redis con latencia — usa try-with-resources para que `getConnection()` no pierda una conexión por probe. |
| `ExternalApiHealthIndicator.java` | Verificación con `java.net.http` con timeouts separados de conexión (2s) y solicitud (3s). |
| `QueueDepthHealthIndicator.java` | Patrón "degradado pero vivo": `UP` con detalle de advertencia antes del umbral, `DOWN` al superarlo. |
| `AvailabilityService.java` | `ApplicationAvailability` + listeners de `AvailabilityChangeEvent`; `markUnready()` drena el pod limpiamente. |
| `ReactiveApiHealthIndicator.java` | `ReactiveHealthIndicator` que devuelve `Mono<Health>` para Spring WebFlux. |
| `CustomStatusIndicator.java` | Registra un `Status("DEGRADED")` personalizado — nota: `@Component` registra el bean, no existe anotación `@HealthIndicator`. |
| `PaymentGatewayClient.java` / `PaymentGatewayStatus.java` / `MessageQueueService.java` | Tipos de apoyo para que los indicadores compilen en contexto. |
| `application.yml` | Exposición de endpoints, `show-details`, `probes.enabled`, grupos personalizados (`infrastructure`/`external`), override de readiness, mapeo HTTP de estados, desactivación de indicadores integrados. |
| `kubernetes-deployment.yml` | `livenessProbe` y `readinessProbe` apuntando a `/actuator/health/liveness` y `/actuator/health/readiness`. |

## Conceptos cubiertos

- **Liveness vs readiness** — liveness responde "¿está viva la JVM?" (reinicio si falla), readiness responde "¿debería recibir tráfico?" (salir de la rotación). Las verificaciones de dependencias van en readiness, nunca en liveness.
- **Los timeouts son parte del check** — Kubernetes trata un timeout de probe igual que un DOWN, así que un check externo lento es un fallo lento.
- **Grupos en configuración** — `management.endpoint.health.group.*` es pura configuración; los nombres de indicadores son los nombres de bean menos el sufijo `HealthIndicator`.
- **DOWN es caro** — reporta `UP` con detalles de advertencia para estados degradados pero funcionales; una caída de un proveedor no debería reiniciar toda tu flota.

## Dependencias

Estas clases van dirigidas a una app Spring Boot 2.3+/3.x con `spring-boot-starter-actuator`, `spring-boot-starter-web` (o `-webflux` para la variante reactiva), `spring-boot-starter-data-redis` y `spring-boot-starter-jdbc` en el classpath:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```
