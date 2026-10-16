// HikariCP reference configuration — sized for a mid-traffic service.
// See https://stackpractices.com/guides/connection-pooling-deep-dive-guide/
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

public class HikariPoolConfig {

    public static HikariDataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:postgresql://db:5432/app");
        config.setUsername("app");
        config.setPassword(System.getenv("DB_PASSWORD"));

        // Pool sizing: pool_size x instance count must fit the DB budget.
        config.setMinimumIdle(5);
        config.setMaximumPoolSize(20);

        // Timeouts: fail fast, close idle connections, rotate before the
        // database or firewall kills them.
        config.setConnectionTimeout(30_000);    // 30s max wait
        config.setIdleTimeout(600_000);         // 10m idle close
        config.setMaxLifetime(1_800_000);       // 30m max age — below DB idle timeout
        config.setValidationTimeout(5_000);     // 5s health check

        // Leak detection: logs the acquisition stack trace for connections
        // held longer than the threshold. Enable in staging first.
        config.setLeakDetectionThreshold(60_000); // 60s warn threshold

        // Prepared-statement cache on the Postgres driver.
        config.setAutoCommit(false);
        config.addDataSourceProperty("cachePrepStmts", "true");
        config.addDataSourceProperty("prepStmtCacheSize", "250");
        config.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");

        return new HikariDataSource(config);
    }
}
