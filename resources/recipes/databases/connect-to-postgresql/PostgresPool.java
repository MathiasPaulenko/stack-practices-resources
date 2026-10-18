import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.*;
import java.util.List;

/**
 * PostgreSQL connection pool with HikariCP.
 * Dependencies: org.postgresql:postgresql, com.zaxxer:HikariCP
 */
public class PostgresPool {
    private static final HikariDataSource ds;

    static {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(System.getenv().getOrDefault(
            "PGJDBC_URL", "jdbc:postgresql://localhost:5432/mydb"));
        config.setUsername(System.getenv().getOrDefault("PGUSER", "user"));
        config.setPassword(System.getenv().getOrDefault("PGPASSWORD", "pass"));
        // Production: config.addDataSourceProperty("sslmode", "verify-full");
        config.addDataSourceProperty("sslmode", "prefer");
        config.setMaximumPoolSize(20);
        config.setMinimumIdle(5);
        config.setIdleTimeout(30000);
        config.setConnectionTimeout(5000);
        ds = new HikariDataSource(config);
    }

    public static Connection getConnection() throws SQLException {
        return ds.getConnection();
    }

    public static void batchInsert(List<String> emails) throws SQLException {
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                 "INSERT INTO users (email) VALUES (?)")) {
            for (String email : emails) {
                stmt.setString(1, email);
                stmt.addBatch();
            }
            stmt.executeBatch();
        }
    }

    public static void main(String[] args) throws SQLException {
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                 "SELECT * FROM users WHERE id = ?")) {
            stmt.setInt(1, 1);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                System.out.println(rs.getString("email"));
            }
        } finally {
            ds.close();
        }
    }
}
