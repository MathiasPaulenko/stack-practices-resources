import java.sql.*;
import java.util.*;

/**
 * Data Mapper pattern demo over JDBC + SQLite.
 *
 * Run:  javac DataMapperDemo.java && java DataMapperDemo
 * Requires the SQLite JDBC driver on the classpath.
 */
class User {
    private Integer id;
    private String name;
    private String email;

    public User() {}
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public void updateEmail(String newEmail) {
        if (!newEmail.contains("@"))
            throw new IllegalArgumentException("Invalid email");
        this.email = newEmail;
    }
}

class UserMapper {
    private final Connection conn;

    public UserMapper(Connection conn) { this.conn = conn; }

    public User findById(int id) throws SQLException {
        try (PreparedStatement stmt = conn.prepareStatement(
                "SELECT id, name, email FROM users WHERE id = ?")) {
            stmt.setInt(1, id);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    User user = new User();
                    user.setId(rs.getInt("id"));
                    user.setName(rs.getString("name"));
                    user.setEmail(rs.getString("email"));
                    return user;
                }
            }
        }
        return null;
    }

    public List<User> findAll() throws SQLException {
        List<User> users = new ArrayList<>();
        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(
                     "SELECT id, name, email FROM users")) {
            while (rs.next()) {
                User user = new User();
                user.setId(rs.getInt("id"));
                user.setName(rs.getString("name"));
                user.setEmail(rs.getString("email"));
                users.add(user);
            }
        }
        return users;
    }

    public void insert(User user) throws SQLException {
        try (PreparedStatement stmt = conn.prepareStatement(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                Statement.RETURN_GENERATED_KEYS)) {
            stmt.setString(1, user.getName());
            stmt.setString(2, user.getEmail());
            stmt.executeUpdate();
            try (ResultSet keys = stmt.getGeneratedKeys()) {
                if (keys.next()) user.setId(keys.getInt(1));
            }
        }
    }

    public void update(User user) throws SQLException {
        try (PreparedStatement stmt = conn.prepareStatement(
                "UPDATE users SET name = ?, email = ? WHERE id = ?")) {
            stmt.setString(1, user.getName());
            stmt.setString(2, user.getEmail());
            stmt.setInt(3, user.getId());
            stmt.executeUpdate();
        }
    }

    public void delete(int id) throws SQLException {
        try (PreparedStatement stmt = conn.prepareStatement(
                "DELETE FROM users WHERE id = ?")) {
            stmt.setInt(1, id);
            stmt.executeUpdate();
        }
    }
}

public class DataMapperDemo {
    public static void main(String[] args) throws SQLException {
        Connection conn = DriverManager.getConnection("jdbc:sqlite::memory:");
        conn.createStatement().execute(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)");


        UserMapper mapper = new UserMapper(conn);
        User user = new User("Alice", "alice@example.com");
        mapper.insert(user);
        System.out.println("Inserted user with ID: " + user.getId());
    }
}
