import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

/**
 * HikariCP connection pool example for PostgreSQL.
 * HikariCP is the standard JVM connection pool used in production.
 */
public class HikariPoolExample {

    private final HikariDataSource ds;

    public HikariPoolExample() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:postgresql://localhost:5432/app");
        config.setUsername("app");
        config.setPassword("secret");
        config.setMaximumPoolSize(20);
        config.setMinimumIdle(5);
        config.setConnectionTimeout(2000);
        config.setIdleTimeout(30000);
        config.setMaxLifetime(1800000);
        config.addDataSourceProperty("cachePrepStmts", "true");
        config.addDataSourceProperty("prepStmtCacheSize", "250");
        this.ds = new HikariDataSource(config);
    }

    public String getUserName(int userId) throws Exception {
        try (Connection conn = ds.getConnection();
             PreparedStatement ps = conn.prepareStatement("SELECT name FROM users WHERE id = ?")) {
            ps.setInt(1, userId);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return rs.getString("name");
                }
                return null;
            }
        }
    }

    public int activeConnections() {
        return ds.getHikariPoolMXBean().getActiveConnections();
    }

    public int idleConnections() {
        return ds.getHikariPoolMXBean().getIdleConnections();
    }

    public int threadsAwaiting() {
        return ds.getHikariPoolMXBean().getThreadsAwaitingConnection();
    }

    public void close() {
        ds.close();
    }

    public static void main(String[] args) throws Exception {
        HikariPoolExample example = new HikariPoolExample();
        try {
            String name = example.getUserName(1);
            System.out.println("User name: " + name);
            System.out.println("Active: " + example.activeConnections());
            System.out.println("Idle: " + example.idleConnections());
            System.out.println("Waiting: " + example.threadsAwaiting());
        } finally {
            example.close();
        }
    }
}