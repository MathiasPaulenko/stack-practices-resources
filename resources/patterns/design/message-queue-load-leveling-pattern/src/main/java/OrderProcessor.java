import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

import java.util.List;

// Load-leveling consumer/producer pair for RabbitMQ.
// Requires a running RabbitMQ broker and a durable "orders" queue.
@Component
public class OrderProcessor {

    private final RabbitTemplate rabbitTemplate;

    public OrderProcessor(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    // Producer: send at any rate
    public void submitOrders(List<Integer> orderIds) {
        for (Integer orderId : orderIds) {
            rabbitTemplate.convertAndSend("orders", "order." + orderId, orderId);
        }
        System.out.println("Enqueued " + orderIds.size() + " orders");
    }

    // Consumer: process one at a time
    @RabbitListener(queues = "orders", concurrency = "1")
    public void processOrder(Integer orderId) {
        try {
            Thread.sleep(2000); // Simulate slow processing
            System.out.println("Processed order " + orderId);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
