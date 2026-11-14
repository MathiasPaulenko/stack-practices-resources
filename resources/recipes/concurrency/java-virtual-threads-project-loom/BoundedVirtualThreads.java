import java.util.concurrent.*;

public class BoundedVirtualThreads {
    public static void main(String[] args) throws InterruptedException {
        // Downstream rate limit: max 10 in-flight calls
        Semaphore semaphore = new Semaphore(10);

        try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 100; i++) {
                final int id = i;
                executor.submit(() -> {
                    semaphore.acquire();
                    try {
                        Thread.sleep(100);
                        System.out.println("Task " + id + " done");
                    } finally {
                        semaphore.release();
                    }
                });
            }
        }
    }
}
