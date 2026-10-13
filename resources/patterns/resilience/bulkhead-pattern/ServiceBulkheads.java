// ServiceBulkheads.java — Java bulkheads using resilience4j.
// Requires: io.github.resilience4j:resilience4j-bulkhead
import io.github.resilience4j.bulkhead.Bulkhead;
import io.github.resilience4j.bulkhead.BulkheadConfig;
import io.github.resilience4j.bulkhead.ThreadPoolBulkhead;
import io.github.resilience4j.bulkhead.ThreadPoolBulkheadConfig;
import java.time.Duration;
import java.util.concurrent.CompletableFuture;

public class ServiceBulkheads {

    // Semaphore-based bulkhead for synchronous calls
    private final Bulkhead paymentBulkhead;
    private final Bulkhead inventoryBulkhead;

    // Thread pool bulkhead for async calls
    private final ThreadPoolBulkhead asyncPaymentBulkhead;

    public ServiceBulkheads() {
        // Payment: max 10 concurrent, 30s wait
        BulkheadConfig paymentConfig = BulkheadConfig.custom()
            .maxConcurrentCalls(10)
            .maxWaitDuration(Duration.ofSeconds(30))
            .build();
        this.paymentBulkhead = Bulkhead.of("payment", paymentConfig);

        // Inventory: max 5 concurrent, 10s wait
        BulkheadConfig inventoryConfig = BulkheadConfig.custom()
            .maxConcurrentCalls(5)
            .maxWaitDuration(Duration.ofSeconds(10))
            .build();
        this.inventoryBulkhead = Bulkhead.of("inventory", inventoryConfig);

        // Async payment: separate thread pool
        ThreadPoolBulkheadConfig asyncConfig = ThreadPoolBulkheadConfig.custom()
            .maxThreadPoolSize(10)
            .coreThreadPoolSize(5)
            .queueCapacity(20)
            .build();
        this.asyncPaymentBulkhead = ThreadPoolBulkhead.of("asyncPayment", asyncConfig);
    }

    public String callPayment(String orderId) {
        return Bulkhead.decorateSupplier(paymentBulkhead, () -> {
            // Payment API call — inject your client here
            return paymentClient.charge(orderId);
        }).get();
    }

    public String callInventory(String productId) {
        return Bulkhead.decorateSupplier(inventoryBulkhead, () -> {
            // Inventory API call — inject your client here
            return inventoryClient.checkStock(productId);
        }).get();
    }

    public CompletableFuture<String> callPaymentAsync(String orderId) {
        return asyncPaymentBulkhead.executeSupplier(() ->
            paymentClient.charge(orderId)
        );
    }
}
