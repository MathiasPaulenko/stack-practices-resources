import java.util.concurrent.*;

public class MixedThreads {
    static void cpuIntensiveTask(int id) {
        long result = 0;
        for (long i = 0; i < 100_000_000L; i++) {
            result += i;
        }
        System.out.println("CPU task " + id + " result: " + result);
    }

    static void ioTask(int id) throws InterruptedException {
        Thread.sleep(500);
        System.out.println("IO task " + id + " done");
    }

    public static void main(String[] args) throws InterruptedException {
        // CPU-bound work stays on a fixed platform pool
        try (ExecutorService cpuPool = Executors.newFixedThreadPool(4);
             // I/O-bound work gets a virtual thread per task
             ExecutorService ioPool = Executors.newVirtualThreadPerTaskExecutor()) {

            for (int i = 0; i < 4; i++) {
                final int id = i;
                cpuPool.submit(() -> cpuIntensiveTask(id));
                ioPool.submit(() -> ioTask(id));
            }

            cpuPool.shutdown();
            ioPool.shutdown();
            cpuPool.awaitTermination(10, TimeUnit.SECONDS);
            ioPool.awaitTermination(10, TimeUnit.SECONDS);
        }

        System.out.println("All tasks completed");
    }
}
