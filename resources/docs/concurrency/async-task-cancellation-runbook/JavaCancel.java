import java.util.concurrent.*;

/**
 * Async task cancellation demo for Java (Future / CompletableFuture).
 *
 * Compile: javac JavaCancel.java
 * Run:     java TaskCancellation
 *
 * future.cancel(true) interrupts the worker thread; the task cooperates by
 * checking Thread.currentThread().isInterrupted() between units of work.
 */
public class JavaCancel {
    public static void main(String[] args) throws Exception {
        ExecutorService executor = Executors.newSingleThreadExecutor();

        Future<String> future = executor.submit(() -> {
            for (int i = 0; i < 1000; i++) {
                if (Thread.currentThread().isInterrupted()) {
                    System.out.println("Task cancelled, cleaning up...");
                    cleanupResources();
                    throw new InterruptedException("Task cancelled");
                }
                Thread.sleep(100);
                System.out.println("Processing item " + i);
            }
            return "done";
        });

        Thread.sleep(2000);
        future.cancel(true);

        try {
            future.get();
        } catch (CancellationException e) {
            System.out.println("Task was cancelled");
        }

        executor.shutdown();
    }

    static void cleanupResources() {
        System.out.println("Closing connections...");
        try {
            Thread.sleep(50);
        } catch (InterruptedException ignored) {
        }
        System.out.println("Cleanup complete");
    }
}
