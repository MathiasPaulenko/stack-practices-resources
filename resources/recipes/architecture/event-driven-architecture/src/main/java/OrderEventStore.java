import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KTable;
import org.apache.kafka.streams.kstream.Materialized;
import org.apache.kafka.streams.kstream.Produced;
import org.apache.kafka.streams.state.QueryableStoreTypes;
import org.apache.kafka.streams.state.ReadOnlyKeyValueStore;
import org.apache.kafka.streams.state.StoreQueryParameters;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

public class OrderEventStore {

    private final KafkaStreams streams;

    public OrderEventStore() {
        StreamsBuilder builder = new StreamsBuilder();

        // Event store: aggregate events by order ID
        KStream<String, OrderEvent> eventStream = builder.stream(
            "orders",
            Consumed.with(Serdes.String(), new OrderEventSerde())
        );

        // Materialize current state from event history
        KTable<String, OrderState> orderState = eventStream
            .groupByKey()
            .aggregate(
                OrderState::new,
                (key, event, state) -> state.apply(event),
                Materialized.as("order-state-store")
            );

        // Project to a read model topic
        orderState.toStream().to("order-read-model",
            Produced.with(Serdes.String(), new OrderStateSerde()));

        streams = new KafkaStreams(builder.build(), getStreamsConfig());
    }

    public void start() {
        streams.start();
    }

    public OrderState getOrder(String orderId) {
        ReadOnlyKeyValueStore<String, OrderState> store =
            streams.store(StoreQueryParameters.fromNameAndType(
                "order-state-store",
                QueryableStoreTypes.keyValueStore()
            ));
        return store.get(orderId);
    }

    public static void main(String[] args) {
        OrderEventStore store = new OrderEventStore();
        Runtime.getRuntime().addShutdownHook(new Thread(store.streams::close));
        store.start();
    }
}

// Apply events to reconstruct state
class OrderState {
    private String status;
    private BigDecimal total;
    private List<String> items = new ArrayList<>();

    public OrderState apply(OrderEvent event) {
        switch (event.getType()) {
            case "OrderPlaced":
                this.status = "placed";
                this.total = event.getTotal();
                this.items = event.getItemIds();
                break;
            case "OrderPaid":
                this.status = "paid";
                break;
            case "OrderShipped":
                this.status = "shipped";
                break;
            case "OrderCancelled":
                this.status = "cancelled";
                break;
        }
        return this;
    }
}
