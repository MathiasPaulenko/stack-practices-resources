import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;

/**
 * Object Pool pattern — Java implementation.
 *
 * Fixed-size pool backed by a BlockingQueue. acquire() waits up to
 * ACQUIRE_TIMEOUT_MS and throws PoolExhaustedException instead of
 * blocking forever. Always release in a finally block (or
 * try-with-resources on a Pool wrapper).
 */
class DatabaseConnection {
    private static int counter = 0;
    private final int id;
    private boolean active = false;

    public DatabaseConnection() {
        this.id = ++counter;
        System.out.println("Created connection " + id + " (expensive)");
    }

    public void open() { this.active = true; }
    public void close() { this.active = false; }

    public String query(String sql) {
        if (!active) throw new IllegalStateException("Not open");
        return "Result for: " + sql;
    }
}

class PoolExhaustedException extends RuntimeException {
    public PoolExhaustedException(String message) { super(message); }
}

public class ConnectionPool {
    private static final long ACQUIRE_TIMEOUT_MS = 5_000;
    private final BlockingQueue<DatabaseConnection> available;

    public ConnectionPool(int size) {
        available = new ArrayBlockingQueue<>(size);
        for (int i = 0; i < size; i++) {
            available.offer(new DatabaseConnection());
        }
    }

    public DatabaseConnection acquire() throws InterruptedException {
        DatabaseConnection conn =
            available.poll(ACQUIRE_TIMEOUT_MS, TimeUnit.MILLISECONDS);
        if (conn == null) {
            throw new PoolExhaustedException(
                "No free objects after " + ACQUIRE_TIMEOUT_MS + "ms");
        }
        conn.open();
        return conn;
    }

    public void release(DatabaseConnection conn) {
        conn.close();
        available.offer(conn);
    }

    public static void main(String[] args) throws InterruptedException {
        ConnectionPool pool = new ConnectionPool(3);

        DatabaseConnection conn = pool.acquire();
        try {
            System.out.println(conn.query("SELECT * FROM users"));
        } finally {
            pool.release(conn);
        }

        // Reuses the same object — no new "(expensive)" line
        DatabaseConnection conn2 = pool.acquire();
        try {
            System.out.println(conn2.query("SELECT * FROM orders"));
        } finally {
            pool.release(conn2);
        }
    }
}
