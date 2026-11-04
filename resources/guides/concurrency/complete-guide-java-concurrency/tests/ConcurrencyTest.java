import static org.junit.jupiter.api.Assertions.assertEquals;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

/** Tests assert invariants under contention, not scheduling. */
class ConcurrencyTest {

    @Test
    void testConcurrentIncrement() throws Exception {
        AtomicInteger counter = new AtomicInteger(0);
        int threads = 100, perThread = 1000;
        ExecutorService executor = Executors.newFixedThreadPool(threads);
        CountDownLatch latch = new CountDownLatch(threads);

        for (int i = 0; i < threads; i++) {
            executor.submit(() -> {
                for (int j = 0; j < perThread; j++) counter.incrementAndGet();
                latch.countDown();
            });
        }
        latch.await(10, TimeUnit.SECONDS);
        executor.shutdown();
        assertEquals(threads * perThread, counter.get());
    }

    @Test
    void testCompletableFuture() throws Exception {
        CompletableFuture<String> future = CompletableFuture
            .supplyAsync(() -> "hello")
            .thenApply(String::toUpperCase)
            .thenApply(s -> s + " world");
        assertEquals("HELLO world", future.get(5, TimeUnit.SECONDS));
    }
}
