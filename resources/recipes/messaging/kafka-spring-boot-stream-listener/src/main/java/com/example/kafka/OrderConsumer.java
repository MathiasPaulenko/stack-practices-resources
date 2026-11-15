package com.example.kafka;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.Backoff;
import org.springframework.kafka.annotation.DltHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.annotation.RetryableTopic;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Service;

@Service
public class OrderConsumer {

    private static final Logger log = LoggerFactory.getLogger(OrderConsumer.class);

    @RetryableTopic(
        attempts = "4",
        backoff = @Backoff(delay = 1000, multiplier = 2.0),
        dltTopicSuffix = "-dlt",
        autoCreateTopics = "true"
    )
    @KafkaListener(topics = "orders", groupId = "order-service")
    public void handleOrder(ConsumerRecord<String, OrderEvent> record, Acknowledgment ack) {
        OrderEvent event = record.value();
        log.info("Processing order {} (partition {}, offset {})",
            event.getOrderId(), record.partition(), record.offset());
        processOrder(event);
        ack.acknowledge();
    }

    @DltHandler
    public void onDlt(OrderEvent event,
                      @Header(KafkaHeaders.RECEIVED_TOPIC) String topic) {
        log.error("Order {} landed in {} after all retries", event.getOrderId(), topic);
    }

    private void processOrder(OrderEvent event) {
        if (event.getOrderId() == null) {
            throw new IllegalArgumentException("Missing orderId");
        }
        if (event.getTotal() < 0) {
            throw new IllegalArgumentException("Negative total");
        }
    }
}
