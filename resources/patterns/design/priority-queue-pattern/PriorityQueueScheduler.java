import java.util.Comparator;
import java.util.concurrent.*;

/**
 * Priority Queue Pattern: PriorityBlockingQueue with a thread pool.
 * Compile: javac PriorityQueueScheduler.java
 * Run: java PriorityQueueScheduler
 */
public class PriorityQueueScheduler {

    private final PriorityBlockingQueue<PriorityTask> queue;
    private final ExecutorService executor;

    public PriorityQueueScheduler(int numWorkers) {
        this.queue = new PriorityBlockingQueue<>(1000, Comparator
            .comparingInt(PriorityTask::getPriority)
            .thenComparingLong(PriorityTask::getTimestamp));
        this.executor = Executors.newFixedThreadPool(numWorkers);
        startWorkers(numWorkers);
    }

    private void startWorkers(int numWorkers) {
        for (int i = 0; i < numWorkers; i++) {
            executor.submit(this::workerLoop);
        }
    }

    private void workerLoop() {
        while (!Thread.currentThread().isInterrupted()) {
            try {
                PriorityTask task = queue.take();
                processTask(task);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }

    private void processTask(PriorityTask task) {
        System.out.printf("Processing [%s] priority=%d%n", task.getTaskId(), task.getPriority());
        try {
            task.getHandler().run();
        } catch (Exception e) {
            System.err.println("Task failed: " + task.getTaskId() + " - " + e.getMessage());
        }
    }

    public void submit(String taskId, Runnable handler, Priority priority) {
        queue.offer(new PriorityTask(taskId, priority.value, handler));
    }

    public void shutdown() {
        executor.shutdown();
    }

    enum Priority {
        CRITICAL(1), HIGH(2), NORMAL(3), LOW(4), BACKGROUND(5);
        final int value;
        Priority(int value) { this.value = value; }
    }

    static class PriorityTask {
        private final String taskId;
        private final int priority;
        private final Runnable handler;
        private final long timestamp = System.currentTimeMillis();

        PriorityTask(String taskId, int priority, Runnable handler) {
            this.taskId = taskId;
            this.priority = priority;
            this.handler = handler;
        }

        public int getPriority() { return priority; }
        public long getTimestamp() { return timestamp; }
        public String getTaskId() { return taskId; }
        public Runnable getHandler() { return handler; }
    }

    public static void main(String[] args) throws InterruptedException {
        PriorityQueueScheduler scheduler = new PriorityQueueScheduler(2);

        scheduler.submit("report-gen", () -> System.out.println("Generating report..."), Priority.NORMAL);
        scheduler.submit("fraud-check", () -> System.out.println("Checking fraud..."), Priority.CRITICAL);
        scheduler.submit("data-cleanup", () -> System.out.println("Cleaning up..."), Priority.BACKGROUND);
        scheduler.submit("vip-request", () -> System.out.println("VIP request..."), Priority.HIGH);

        Thread.sleep(2000);
        scheduler.shutdown();
    }
}
