import java.io.IOException;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Recursive directory watcher using Java NIO WatchService.
 * Registers every subdirectory up front and auto-registers new ones.
 * Handles OVERFLOW events and invalid keys explicitly.
 *
 * Usage: javac RecursiveWatcher.java && java RecursiveWatcher ./src
 */
public class RecursiveWatcher {

    private final WatchService watchService;
    private final ExecutorService executor;
    private final AtomicBoolean running = new AtomicBoolean(true);
    private final ConcurrentHashMap<WatchKey, Path> keys = new ConcurrentHashMap<>();

    public RecursiveWatcher() throws Exception {
        this.watchService = FileSystems.getDefault().newWatchService();
        this.executor = Executors.newSingleThreadExecutor();
    }

    public void registerAll(Path start) throws Exception {
        Files.walkFileTree(start, new SimpleFileVisitor<>() {
            @Override
            public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
                WatchKey key = dir.register(watchService,
                    StandardWatchEventKinds.ENTRY_CREATE,
                    StandardWatchEventKinds.ENTRY_MODIFY,
                    StandardWatchEventKinds.ENTRY_DELETE);
                keys.put(key, dir);
                return FileVisitResult.CONTINUE;
            }
        });
    }

    public void start() {
        executor.submit(() -> {
            while (running.get()) {
                try {
                    WatchKey key = watchService.poll(1, TimeUnit.SECONDS);
                    if (key == null) continue;

                    Path dir = keys.get(key);
                    if (dir == null) {
                        key.reset();
                        continue;
                    }
                    for (WatchEvent<?> event : key.pollEvents()) {
                        if (event.kind() == StandardWatchEventKinds.OVERFLOW) {
                            continue; // events lost; rescan dir if exactness matters
                        }
                        Path fullPath = dir.resolve((Path) event.context());
                        System.out.println(event.kind() + ": " + fullPath);

                        // Auto-register new subdirectories
                        if (event.kind() == StandardWatchEventKinds.ENTRY_CREATE
                                && Files.isDirectory(fullPath)) {
                            registerAll(fullPath);
                        }
                    }
                    if (!key.reset()) {
                        keys.remove(key); // directory no longer accessible
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });
    }

    public void stop() throws Exception {
        running.set(false);
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
        watchService.close();
    }

    public static void main(String[] args) throws Exception {
        Path dir = args.length > 0 ? Path.of(args[0]) : Path.of("./src");
        RecursiveWatcher watcher = new RecursiveWatcher();
        watcher.registerAll(dir);
        watcher.start();
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            try { watcher.stop(); } catch (Exception ignored) {}
        }));
        System.out.println("Watching " + dir + " (Ctrl+C to stop)");
    }
}
