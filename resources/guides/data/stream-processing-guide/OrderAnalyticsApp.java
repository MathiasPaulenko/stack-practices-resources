// Example: Kafka Streams application for order analytics
public class OrderAnalyticsApp {
    
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "order-analytics");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, 
            Serdes.String().getClass().getName());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, 
            Serdes.String().getClass().getName());
        
        StreamsBuilder builder = new StreamsBuilder();
        
        // Read order events
        KStream<String, Order> orders = builder.stream("orders",
            Consumed.with(Serdes.String(), new OrderSerde()));
        
        // Filter high-value orders
        KStream<String, Order> highValueOrders = orders
            .filter((key, order) -> order.getTotal() > 100.0);
        
        // Enrich with customer data (KTable lookup)
        KTable<String, Customer> customers = builder.table("customers",
            Consumed.with(Serdes.String(), new CustomerSerde()));
        
        KStream<String, EnrichedOrder> enrichedOrders = highValueOrders
            .leftJoin(customers, (order, customer) -> new EnrichedOrder(order, customer));
        
        // Write to output topic
        enrichedOrders.to("enriched-orders",
            Produced.with(Serdes.String(), new EnrichedOrderSerde()));
        
        // Tumbling window: revenue per category per hour
        orders
            .groupBy((key, order) -> order.getCategory())
            .windowedBy(TimeWindows.of(Duration.ofHours(1)))
            .aggregate(
                () -> 0.0,
                (key, order, total) -> total + order.getTotal(),
                Materialized.with(Serdes.String(), Serdes.Double())
            )
            .toStream()
            .to("hourly-revenue-by-category");
        
        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();
        
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
