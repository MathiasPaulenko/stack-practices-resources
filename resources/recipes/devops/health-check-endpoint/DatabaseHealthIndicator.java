import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;
import java.sql.Connection;

/**
 * Database health indicator for the Spring Boot Actuator readiness group.
 *
 * Spring Boot 2.3+ already exposes /actuator/health/liveness and
 * /actuator/health/readiness when management.endpoint.health.probes.enabled=true.
 * Register this bean and reference it from the readiness group to include
 * the database in the readiness result:
 *
 *   management.endpoint.health.group.readiness.include=db
 */
@Component
public class DatabaseHealthIndicator implements HealthIndicator {
    private final DataSource dataSource;

    public DatabaseHealthIndicator(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Health health() {
        try (Connection conn = dataSource.getConnection()) {
            if (conn.isValid(2)) {
                return Health.up().withDetail("database", "reachable").build();
            }
        } catch (Exception e) {
            return Health.down().withException(e).build();
        }
        return Health.down().withDetail("database", "timeout").build();
    }
}
