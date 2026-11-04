import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;
import java.time.Duration;
import java.util.Properties;

// Streams topology from the guide: branch, filter, aggregate, join.
public class OrderStreamProcessor {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put("application.id", "order-processor");
        props.put("bootstrap.servers", "localhost:9092");
        props.put("default.key.serde", "org.apache.kafka.common.serialization.Serdes$StringSerde");
        props.put("default.value.serde", "org.apache.kafka.common.serialization.Serdes$StringSerde");
        props.put("processing.guarantee", "exactly_once_v2");

        StreamsBuilder builder = new StreamsBuilder();
        KStream<String, String> orders = builder.stream("orders");

        KStream<String, String>[] branches = orders.branch(
            (key, value) -> value.contains("\"amount\":0"),
            (key, value) -> true
        );

        branches[1].filter((k, v) -> v.contains("\"amount\":1"))
            .to("high-value-orders");
        branches[1].to("processed-orders");

        KTable<Windowed<String>, Long> windowedCounts = orders
            .groupByKey()
            .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
            .count();
        windowedCounts.toStream((k, v) -> k.key() + "@" + k.window().start())
            .to("windowed-order-counts");

        new KafkaStreams(builder.build(), props).start();
    }
}
