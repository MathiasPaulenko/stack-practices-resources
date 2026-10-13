// Active Record pattern: a User class where each instance is a table row.
// Requires the SQLite JDBC driver on the classpath (org.xerial:sqlite-jdbc).

import java.sql.*;
import java.util.*;

public class ActiveRecordUser {
    private static String dbUrl = "jdbc:sqlite:app.db";

    private int id;
    private String name;
    private String email;

    public ActiveRecordUser() {}

    public ActiveRecordUser(int id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    public void save() {
        try (Connection conn = DriverManager.getConnection(dbUrl)) {
            if (id == 0) {
                PreparedStatement ps = conn.prepareStatement(
                    "INSERT INTO users (name, email) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS);
                ps.setString(1, name);
                ps.setString(2, email);
                ps.executeUpdate();
                ResultSet keys = ps.getGeneratedKeys();
                keys.next();
                id = keys.getInt(1);
            } else {
                PreparedStatement ps = conn.prepareStatement(
                    "UPDATE users SET name = ?, email = ? WHERE id = ?");
                ps.setString(1, name);
                ps.setString(2, email);
                ps.setInt(3, id);
                ps.executeUpdate();
            }
        } catch (SQLException e) { throw new RuntimeException(e); }
    }

    public void delete() {
        try (Connection conn = DriverManager.getConnection(dbUrl)) {
            PreparedStatement ps = conn.prepareStatement("DELETE FROM users WHERE id = ?");
            ps.setInt(1, id);
            ps.executeUpdate();
        } catch (SQLException e) { throw new RuntimeException(e); }
    }

    public static ActiveRecordUser findById(int id) {
        try (Connection conn = DriverManager.getConnection(dbUrl)) {
            PreparedStatement ps = conn.prepareStatement("SELECT id, name, email FROM users WHERE id = ?");
            ps.setInt(1, id);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) return new ActiveRecordUser(rs.getInt(1), rs.getString(2), rs.getString(3));
        } catch (SQLException e) { throw new RuntimeException(e); }
        return null;
    }

    public static List<ActiveRecordUser> findAll() {
        List<ActiveRecordUser> users = new ArrayList<>();
        try (Connection conn = DriverManager.getConnection(dbUrl)) {
            Statement st = conn.createStatement();
            ResultSet rs = st.executeQuery("SELECT id, name, email FROM users");
            while (rs.next()) {
                users.add(new ActiveRecordUser(rs.getInt(1), rs.getString(2), rs.getString(3)));
            }
        } catch (SQLException e) { throw new RuntimeException(e); }
        return users;
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    @Override
    public String toString() {
        return "User{id=" + id + ", name='" + name + "', email='" + email + "'}";
    }
}
