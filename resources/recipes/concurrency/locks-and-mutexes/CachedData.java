import java.util.concurrent.locks.ReentrantReadWriteLock;

class CachedData {
    private String data;
    private boolean cacheValid;
    private final ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();

    public String processData() {
        rwl.readLock().lock();
        if (cacheValid) {
            String result = data;
            rwl.readLock().unlock();
            return result;
        }
        rwl.readLock().unlock();

        rwl.writeLock().lock();
        try {
            if (!cacheValid) {
                data = fetchFromDatabase();
                cacheValid = true;
            }
            return data;
        } finally {
            rwl.writeLock().unlock();
        }
    }

    private String fetchFromDatabase() {
        return "result-" + System.currentTimeMillis();
    }

    public static void main(String[] args) throws InterruptedException {
        CachedData cache = new CachedData();
        Thread[] readers = new Thread[8];
        for (int i = 0; i < readers.length; i++) {
            readers[i] = new Thread(() -> System.out.println(cache.processData()));
            readers[i].start();
        }
        for (Thread t : readers) {
            t.join();
        }
    }
}
