package com.example.kafka;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class SampleOrderProducer implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(SampleOrderProducer.class);

    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;

    public SampleOrderProducer(KafkaTemplate<String, OrderEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    @Override
    public void run(String... args) {
        for (int i = 1; i <= 20; i++) {
            String orderId = "order-" + i;
            // Every 7th event has a negative total -> lands in orders-dlt
            double total = (i % 7 == 0) ? -1.0 : 10.0 * i;
            kafkaTemplate.send("orders", orderId, new OrderEvent(orderId, "user-" + i, total));
        }
        kafkaTemplate.flush();
        log.info("Sent 20 sample orders (2 will fail and go to the DLT)");
    }
}
