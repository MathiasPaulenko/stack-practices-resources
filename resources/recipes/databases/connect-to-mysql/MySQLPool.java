// Connect to MySQL with HikariCP + Connector/J: pool, prepared statement, batch insert.
// Needs mysql-connector-j + HikariCP + slf4j-api on the classpath.
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.*;
import java.util.List;

public class MySQLPool {
    private static final HikariDataSource ds;

    static {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:mysql://localhost:3306/mydb"
            + "?serverTimezone=UTC&connectTimeout=5000&socketTimeout=30000"
            + "&rewriteBatchedStatements=true");
        config.setUsername("user");
        config.setPassword("pass");
        config.setMaximumPoolSize(20);
        config.setMinimumIdle(5);
        config.setIdleTimeout(30000);
        config.setConnectionTimeout(5000);
        config.setKeepaliveTime(300000); // refresh before wait_timeout kills idle conns
        ds = new HikariDataSource(config);
    }

    public static Connection getConnection() throws SQLException {
        return ds.getConnection();
    }

    public static void queryUser(int id) throws SQLException {
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                 "SELECT * FROM users WHERE id = ?")) {
            stmt.setInt(1, id);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                System.out.println(rs.getString("email"));
            }
        }
    }

    public static void batchInsert(List<String> emails) throws SQLException {
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                 "INSERT INTO users (email, name) VALUES (?, ?)")) {
            for (String email : emails) {
                stmt.setString(1, email);
                stmt.setString(2, email.split("@")[0]);
                stmt.addBatch();
            }
            stmt.executeBatch(); // fast thanks to rewriteBatchedStatements=true
        }
    }

    public static void main(String[] args) throws SQLException {
        queryUser(1);
        batchInsert(List.of("new@example.com"));
        ds.close();
    }
}
