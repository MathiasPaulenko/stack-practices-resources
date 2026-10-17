import org.springframework.stereotype.Service;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.kafka.core.KafkaTemplate;

@Service
public class OutboxPublisher {

    private final JdbcTemplate jdbc;
    private final KafkaTemplate<String, String> kafka;

    public OutboxPublisher(JdbcTemplate jdbc, KafkaTemplate<String, String> kafka) {
        this.jdbc = jdbc;
        this.kafka = kafka;
    }

    @Scheduled(fixedDelay = 1000)
    public void publishPendingEvents() {
        var events = jdbc.queryForList(
            "SELECT id, aggregate_id, event_type, payload FROM outbox WHERE published = false LIMIT 100"
        );

        for (var event : events) {
            kafka.send("order." + event.get("event_type"),
                       (String) event.get("aggregate_id"),
                       (String) event.get("payload"));
            jdbc.update("UPDATE outbox SET published = true WHERE id = ?", event.get("id"));
        }
    }
}
