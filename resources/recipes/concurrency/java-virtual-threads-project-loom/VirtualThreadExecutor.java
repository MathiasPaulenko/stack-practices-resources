import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.stream.IntStream;

public class VirtualThreadExecutor {
    public static void main(String[] args) throws InterruptedException {
        // One virtual thread per task — don't pool them
        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {

            IntStream.range(0, 10_000).forEach(i -> {
                executor.submit(() -> {
                    try {
                        TimeUnit.MILLISECONDS.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    return i * 2;
                });
            });

            // try-with-resources blocks until every task finishes
        }

        System.out.println("All 10,000 virtual threads completed");
    }
}
