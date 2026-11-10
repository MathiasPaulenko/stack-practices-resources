import java.sql.*;
import java.util.Collections;
import java.util.List;

/**
 * Safe raw SQL with JDBC PreparedStatement. Parameterize values, whitelist identifiers.
 */
public class RawSQL {

    public void findUser(Connection conn, String email) throws SQLException {
        String sql = "SELECT * FROM users WHERE email = ? AND active = ?";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, email);
            stmt.setBoolean(2, true);
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    System.out.println(rs.getString("email"));
                }
            }
        }
    }

    public int createUser(Connection conn, String email, String role) throws SQLException {
        String sql = "INSERT INTO users (email, role) VALUES (?, ?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            stmt.setString(1, email);
            stmt.setString(2, role);
            stmt.executeUpdate();
            try (ResultSet keys = stmt.getGeneratedKeys()) {
                keys.next();
                return keys.getInt(1);
            }
        }
    }

    /** Dynamic IN clause: build one ? per element and bind each by position. */
    public ResultSet findByEmails(Connection conn, List<String> emails) throws SQLException {
        String placeholders = String.join(",", Collections.nCopies(emails.size(), "?"));
        String sql = "SELECT * FROM users WHERE email IN (" + placeholders + ")";
        PreparedStatement stmt = conn.prepareStatement(sql);
        for (int i = 0; i < emails.size(); i++) {
            stmt.setString(i + 1, emails.get(i));
        }
        return stmt.executeQuery();
    }
}
