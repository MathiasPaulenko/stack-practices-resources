import org.springframework.amqp.core.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Queue-Based Load Leveling Pattern - RabbitMQ configuration.
 *
 * Defines the main task queue with depth limit, overflow behavior,
 * message TTL, and a dead-letter queue for failed messages.
 */
@Configuration
public class QueueConfig {

    @Bean
    Queue deadLetterQueue() {
        return QueueBuilder.durable("task-dlq").build();
    }

    @Bean
    Queue taskQueue() {
        return QueueBuilder.durable("task-queue")
            .withArgument("x-max-length", 10000)
            .withArgument("x-overflow", "reject-publish")
            .withArgument("x-message-ttl", 3600000)
            .withArgument("x-dead-letter-exchange", "task-dlx")
            .withArgument("x-dead-letter-routing-key", "task.dead")
            .build();
    }

    @Bean
    DirectExchange exchange() {
        return new DirectExchange("task-exchange");
    }

    @Bean
    DirectExchange deadLetterExchange() {
        return new DirectExchange("task-dlx");
    }

    @Bean
    Binding binding(Queue taskQueue, DirectExchange exchange) {
        return BindingBuilder.bind(taskQueue).to(exchange).with("task.routing.key");
    }

    @Bean
    Binding dlqBinding(Queue deadLetterQueue, DirectExchange deadLetterExchange) {
        return BindingBuilder.bind(deadLetterQueue).to(deadLetterExchange).with("task.dead");
    }
}
