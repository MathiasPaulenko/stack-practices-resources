// ResourceCleanupHook.java — Custom shutdown hook for resource cleanup
import org.springframework.context.SmartLifecycle;
import org.springframework.stereotype.Component;

@Component
public class ResourceCleanupHook implements SmartLifecycle {

    private volatile boolean running = false;

    @Override
    public void start() {
        running = true;
    }

    @Override
    public void stop() {
        running = false;
        // Close database connections
        closeDatabaseConnections();
        // Flush log buffers
        flushLogBuffers();
        // Close message consumer connections
        closeMessageConsumers();
        System.out.println("Resource cleanup complete");
    }

    @Override
    public boolean isRunning() {
        return running;
    }

    @Override
    public int getPhase() {
        // Run cleanup early in shutdown sequence
        return Integer.MIN_VALUE + 100;
    }

    private void closeDatabaseConnections() {
        System.out.println("Closing database connections...");
    }

    private void flushLogBuffers() {
        System.out.println("Flushing log buffers...");
    }

    private void closeMessageConsumers() {
        System.out.println("Closing message consumers...");
    }
}
