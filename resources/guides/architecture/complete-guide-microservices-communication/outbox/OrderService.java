import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.jdbc.core.JdbcTemplate;

@Service
public class OrderService {

    private final JdbcTemplate jdbc;

    public OrderService(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @Transactional
    public void createOrder(Order order) {
        // 1. Save order
        jdbc.update(
            "INSERT INTO orders (id, customer_id, total) VALUES (?, ?, ?)",
            order.getId(), order.getCustomerId(), order.getTotal()
        );

        // 2. Save outbox event in the same transaction
        jdbc.update(
            "INSERT INTO outbox (aggregate_id, event_type, payload) VALUES (?, ?, ?)",
            order.getId(), "OrderCreated", order.toJson()
        );
    }
}
