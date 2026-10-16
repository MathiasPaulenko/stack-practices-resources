// PostgresIntegrationTest.java — Database integration test
import org.junit.jupiter.api.*;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import static org.junit.jupiter.api.Assertions.*;
import java.sql.*;

@Testcontainers
class PostgresIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test")
        .withReuse(true); // Reuse across test runs for speed

    private Connection connection;

    @BeforeEach
    void setUp() throws SQLException {
        connection = DriverManager.getConnection(
            postgres.getJdbcUrl(),
            postgres.getUsername(),
            postgres.getPassword()
        );
        try (Statement stmt = connection.createStatement()) {
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """);
        }
    }

    @AfterEach
    void tearDown() throws SQLException {
        try (Statement stmt = connection.createStatement()) {
            stmt.execute("DROP TABLE IF EXISTS users");
        }
        connection.close();
    }

    @Test
    void testInsertAndQuery() throws SQLException {
        try (PreparedStatement ps = connection.prepareStatement(
            "INSERT INTO users (email, name) VALUES (?, ?) RETURNING id"
        )) {
            ps.setString(1, "alice@example.com");
            ps.setString(2, "Alice");
            ResultSet rs = ps.executeQuery();
            assertTrue(rs.next());
            int id = rs.getInt("id");
            assertTrue(id > 0);
        }

        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT COUNT(*) FROM users")) {
            assertTrue(rs.next());
            assertEquals(1, rs.getInt(1));
        }
    }

    @Test
    void testUniqueConstraint() throws SQLException {
        try (PreparedStatement ps = connection.prepareStatement(
            "INSERT INTO users (email, name) VALUES (?, ?)"
        )) {
            ps.setString(1, "bob@example.com");
            ps.setString(2, "Bob");
            ps.executeUpdate();
        }

        // Duplicate email should fail
        SQLException ex = assertThrows(SQLException.class, () -> {
            try (PreparedStatement ps = connection.prepareStatement(
                "INSERT INTO users (email, name) VALUES (?, ?)"
            )) {
                ps.setString(1, "bob@example.com");
                ps.setString(2, "Bob 2");
                ps.executeUpdate();
            }
        });
        assertTrue(ex.getMessage().contains("unique constraint"));
    }
}
