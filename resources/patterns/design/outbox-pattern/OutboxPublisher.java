import java.sql.*;
import java.time.Instant;

public class OutboxPublisher {
    private final Connection conn;

    public OutboxPublisher(Connection conn) {
        this.conn = conn;
    }

    public void publish(String aggregateType, String aggregateId,
                        String eventType, String payload) throws SQLException {
        try (PreparedStatement ps = conn.prepareStatement(
            "INSERT INTO outbox (aggregate_type, aggregate_id, event_type, payload) VALUES (?, ?, ?, ?)")) {
            ps.setString(1, aggregateType);
            ps.setString(2, aggregateId);
            ps.setString(3, eventType);
            ps.setString(4, payload);
            ps.executeUpdate();
        }
    }
}

public class OrderService {
    private final Connection conn;
    private final OutboxPublisher outbox;

    public OrderService(Connection conn, OutboxPublisher outbox) {
        this.conn = conn;
        this.outbox = outbox;
    }

    public void placeOrder(String userId, String productId, double amount) throws SQLException {
        conn.setAutoCommit(false);
        try {
            long orderId;
            try (PreparedStatement ps = conn.prepareStatement(
                "INSERT INTO orders (user_id, product_id, amount) VALUES (?, ?, ?)", Statement.RETURN_GENERATED_KEYS)) {
                ps.setString(1, userId);
                ps.setString(2, productId);
                ps.setDouble(3, amount);
                ps.executeUpdate();
                ResultSet rs = ps.getGeneratedKeys();
                rs.next();
                orderId = rs.getLong(1);
            }

            outbox.publish("Order", String.valueOf(orderId), "OrderPlaced",
                String.format("{\"user_id\":\"%s\",\"product_id\":\"%s\",\"amount\":%f}", userId, productId, amount));

            conn.commit();
        } catch (Exception e) {
            conn.rollback();
            throw e;
        }
    }
}
