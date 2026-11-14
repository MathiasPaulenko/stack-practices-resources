import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.HealthIndicator;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    private final JdbcTemplate jdbcTemplate;

    public DatabaseHealthIndicator(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Override
    public Health health() {
        try {
            Integer result = jdbcTemplate.queryForObject("SELECT 1", Integer.class);
            int activeConnections = jdbcTemplate.queryForObject(
                "SELECT count(*) FROM pg_stat_activity WHERE state = 'active'",
                Integer.class
            );

            return Health.up()
                .withDetail("database", "postgresql")
                .withDetail("active_connections", activeConnections)
                .withDetail("max_connections", 100)
                .build();
        } catch (Exception e) {
            return Health.down(e)
                .withDetail("database", "postgresql")
                .withDetail("error", "Connection failed")
                .build();
        }
    }
}
