import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

// Factory Pattern: registry-based factory for database connections.
public class DatabaseFactory {

    public interface DatabaseConnection {
        String connect();
        String query(String sql);
    }

    public static class PostgresConnection implements DatabaseConnection {
        private final String dsn;

        public PostgresConnection(Map<String, String> cfg) {
            this.dsn = "postgresql://" + cfg.get("host") + ":" + cfg.get("port") + "/" + cfg.get("database");
        }

        public String connect() {
            return "pg.connect(" + dsn + ")";
        }

        public String query(String sql) {
            return "pg.query(" + sql + ")";
        }
    }

    public static class MySQLConnection implements DatabaseConnection {
        private final String dsn;

        public MySQLConnection(Map<String, String> cfg) {
            this.dsn = "mysql://" + cfg.get("host") + ":" + cfg.get("port") + "/" + cfg.get("database");
        }

        public String connect() {
            return "mysql.connect(" + dsn + ")";
        }

        public String query(String sql) {
            return "mysql.query(" + sql + ")";
        }
    }

    private static final Map<String, Function<Map<String, String>, DatabaseConnection>> REGISTRY = new HashMap<>();

    static {
        REGISTRY.put("postgres", PostgresConnection::new);
        REGISTRY.put("mysql", MySQLConnection::new);
    }

    public static DatabaseConnection create(String type, Map<String, String> config) {
        Function<Map<String, String>, DatabaseConnection> creator = REGISTRY.get(type);
        if (creator == null) {
            throw new IllegalArgumentException("Unknown DB type: " + type);
        }
        return creator.apply(config);
    }

    public static void main(String[] args) {
        Map<String, String> cfg = Map.of("host", "localhost", "port", "5432", "database", "myapp");
        DatabaseConnection db = DatabaseFactory.create("postgres", cfg);
        System.out.println(db.connect());
        System.out.println(db.query("SELECT * FROM users"));
    }
}
