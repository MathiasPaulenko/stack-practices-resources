import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.*;

public class HikariLambda implements RequestHandler<Request, Response> {
    // One connection per container; PgBouncer multiplexes server-side.
    private static final HikariDataSource dataSource = createDataSource();

    private static HikariDataSource createDataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:postgresql://" + System.getenv("DB_HOST")
            + ":" + System.getenv("DB_PORT") + "/" + System.getenv("DB_NAME"));
        config.setUsername(System.getenv("DB_USER"));
        config.setPassword(System.getenv("DB_PASSWORD"));
        config.setMaximumPoolSize(1);
        config.setMinimumIdle(0);
        config.setIdleTimeout(30000);
        config.setConnectionTimeout(3000);
        config.setPrepareThreshold(0); // PgBouncer transaction pooling breaks prepared statements
        return new HikariDataSource(config);
    }

    @Override
    public Response handleRequest(Request request, Context context) {
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement(
                 "SELECT id, email FROM users WHERE id = ?")) {
            ps.setLong(1, request.getUserId());
            ResultSet rs = ps.executeQuery();
            return rs.next()
                ? new Response(rs.getLong("id"), rs.getString("email"))
                : new Response(-1, "not found");
        } catch (SQLException e) {
            throw new RuntimeException("DB error", e);
        }
    }
}
