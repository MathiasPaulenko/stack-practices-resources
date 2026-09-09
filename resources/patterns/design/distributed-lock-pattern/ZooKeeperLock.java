import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.recipes.locks.InterProcessMutex;
import org.apache.curator.retry.ExponentialBackoffRetry;
import java.util.concurrent.TimeUnit;

/**
 * Distributed lock using ZooKeeper via Apache Curator.
 */
public class ZooKeeperLock {

    private final CuratorFramework client;
    private final String lockPath;

    public ZooKeeperLock(String zkConnectionString, String lockPath) {
        this.lockPath = lockPath;
        this.client = CuratorFrameworkFactory.newClient(
            zkConnectionString,
            new ExponentialBackoffRetry(1000, 3)
        );
        this.client.start();
    }

    public void executeWithLock(Runnable task, long timeout, TimeUnit unit) throws Exception {
        InterProcessMutex mutex = new InterProcessMutex(client, lockPath);

        if (mutex.acquire(timeout, unit)) {
            try {
                task.run();
            } finally {
                mutex.release();
            }
        } else {
            throw new RuntimeException("Could not acquire lock within timeout");
        }
    }

    public void close() {
        client.close();
    }

    public static void main(String[] args) throws Exception {
        ZooKeeperLock lock = new ZooKeeperLock("localhost:2181", "/locks/daily-report");

        lock.executeWithLock(() -> {
            System.out.println("Processing daily report...");
            try { Thread.sleep(2000); } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            System.out.println("Report processing complete");
        }, 10, TimeUnit.SECONDS);

        lock.close();
    }
}
