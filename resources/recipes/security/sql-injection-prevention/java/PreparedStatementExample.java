import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Map;
import java.util.Set;
import javax.sql.DataSource;

/**
 * PreparedStatement examples: '?' placeholders bind input as data.
 * Inject your container's DataSource — the code never concatenates
 * untrusted values into SQL.
 */
public class PreparedStatementExample {

    private final DataSource dataSource;

    public PreparedStatementExample(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public void printActiveUserByEmail(String email) throws SQLException {
        // SAFE — parameters bind to the driver, not the query string
        String sql = "SELECT name FROM users WHERE email = ? AND active = ?";
        try (Connection conn = dataSource.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, email);
            stmt.setBoolean(2, true);
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    System.out.println(rs.getString("name"));
                }
            }
        }
    }

    private static final Set<String> ALLOWED_SORT_COLUMNS =
            Set.of("name", "email", "created_at");
    private static final Map<String, String> DIRECTIONS =
            Map.of("ASC", "ASC", "DESC", "DESC");

    public ResultSet listUsers(DataSource ds, String sortBy, String sortDir)
            throws SQLException {
        String column = ALLOWED_SORT_COLUMNS.contains(sortBy) ? sortBy : "created_at";
        String direction = DIRECTIONS.getOrDefault(sortDir.toUpperCase(), "DESC");
        String sql = "SELECT id, name, email, created_at FROM users "
                + "WHERE active = TRUE ORDER BY " + column + " " + direction
                + " LIMIT ?";
        Connection conn = ds.getConnection();
        PreparedStatement stmt = conn.prepareStatement(sql);
        stmt.setInt(1, 20);
        return stmt.executeQuery();
    }
}
