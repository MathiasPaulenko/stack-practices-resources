import java.sql.*;
import java.util.*;

/**
 * Runnable DAO demo for the users table over JDBC.
 *
 * Split User, UserDao, DataAccessException and SqlUserDao into their own
 * public files in a real project — they're merged here so the example
 * compiles as a single file:
 *
 *   javac SqlUserDao.java && java -cp ".:sqlite-jdbc.jar" SqlUserDao
 *
 * Requires an SQLite JDBC driver on the classpath (org.xerial:sqlite-jdbc).
 * In production, hand the DAO a connection from a pool (HikariCP / DataSource).
 */
record User(int id, String name, String email) {}

interface UserDao {
    Optional<User> findById(int id);
    List<User> findAll();
    User save(User user);
    void delete(int id);
}

class DataAccessException extends RuntimeException {
    DataAccessException(Throwable cause) { super(cause); }
}

public class SqlUserDao implements UserDao {
    private final Connection conn;

    public SqlUserDao(Connection conn) {
        this.conn = conn;
    }

    public Optional<User> findById(int id) {
        try (PreparedStatement ps = conn.prepareStatement(
            "SELECT id, name, email FROM users WHERE id = ?")) {
            ps.setInt(1, id);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) {
                return Optional.of(mapRow(rs));
            }
            return Optional.empty();
        } catch (SQLException e) {
            throw new DataAccessException(e);
        }
    }

    public List<User> findAll() {
        List<User> users = new ArrayList<>();
        try (Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT id, name, email FROM users")) {
            while (rs.next()) {
                users.add(mapRow(rs));
            }
            return users;
        } catch (SQLException e) {
            throw new DataAccessException(e);
        }
    }

    public User save(User user) {
        try (PreparedStatement ps = conn.prepareStatement(
            "INSERT INTO users (name, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, user.name());
            ps.setString(2, user.email());
            ps.executeUpdate();
            ResultSet keys = ps.getGeneratedKeys();
            keys.next();
            return new User(keys.getInt(1), user.name(), user.email());
        } catch (SQLException e) {
            throw new DataAccessException(e);
        }
    }

    public void delete(int id) {
        try (PreparedStatement ps = conn.prepareStatement(
            "DELETE FROM users WHERE id = ?")) {
            ps.setInt(1, id);
            ps.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException(e);
        }
    }

    private User mapRow(ResultSet rs) throws SQLException {
        return new User(rs.getInt("id"), rs.getString("name"), rs.getString("email"));
    }

    public static void main(String[] args) throws SQLException {
        Connection conn = DriverManager.getConnection("jdbc:sqlite::memory:");
        try (Statement st = conn.createStatement()) {
            st.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)");
        }

        UserDao dao = new SqlUserDao(conn);
        User alice = dao.save(new User(0, "Alice", "alice@example.com"));
        User bob = dao.save(new User(0, "Bob", "bob@example.com"));

        System.out.println("findById: " + dao.findById(alice.id()));
        System.out.println("findAll: " + dao.findAll());

        dao.delete(bob.id());
        System.out.println("after delete: " + dao.findAll());
    }
}
