import java.io.*;
import java.nio.file.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;
import java.util.function.Function;

public class ParallelStreamProcessor {

    private final ExecutorService executor;
    private final int batchSize;

    public ParallelStreamProcessor(int workers, int batchSize) {
        this.executor = Executors.newFixedThreadPool(workers);
        this.batchSize = batchSize;
    }

    public void process(String input, String output, Function<String, String> transformer)
            throws Exception {
        Path tmpPath = Path.of(output + ".tmp");
        AtomicLong processed = new AtomicLong(0);
        long startTime = System.currentTimeMillis();

        try (BufferedReader reader = Files.newBufferedReader(Path.of(input));
             BufferedWriter writer = Files.newBufferedWriter(tmpPath)) {

            // Read in batches, process in parallel, write sequentially
            String[] batch = new String[batchSize];
            int batchIndex = 0;
            String line;

            while ((line = reader.readLine()) != null) {
                batch[batchIndex++] = line;
                if (batchIndex == batchSize) {
                    String[] results = processBatch(batch, batchIndex, transformer);
                    for (int i = 0; i < batchIndex; i++) {
                        if (results[i] != null) {
                            writer.write(results[i]);
                            writer.newLine();
                        }
                        long count = processed.incrementAndGet();
                        if (count % 10000 == 0) {
                            double elapsed = (System.currentTimeMillis() - startTime) / 1000.0;
                            System.out.printf("  Processed %d lines (%.0f/s)%n",
                                count, count / elapsed);
                        }
                    }
                    batchIndex = 0;
                }
            }

            // Process remaining lines in final partial batch
            if (batchIndex > 0) {
                String[] results = processBatch(batch, batchIndex, transformer);
                for (int i = 0; i < batchIndex; i++) {
                    if (results[i] != null) {
                        writer.write(results[i]);
                        writer.newLine();
                    }
                }
            }
        }

        Files.move(tmpPath, Path.of(output), StandardCopyOption.ATOMIC_MOVE);
        long total = processed.get();
        double elapsed = (System.currentTimeMillis() - startTime) / 1000.0;
        System.out.printf("Done: %d lines in %.1fs (%.0f/s)%n", total, elapsed, total / elapsed);
    }

    private String[] processBatch(String[] batch, int size, Function<String, String> transformer)
            throws Exception {
        Future<String>[] futures = new Future[size];
        for (int i = 0; i < size; i++) {
            final String line = batch[i];
            futures[i] = executor.submit(() -> transformer.apply(line));
        }
        String[] results = new String[size];
        for (int i = 0; i < size; i++) {
            results[i] = futures[i].get();
        }
        return results;
    }

    public void shutdown() {
        executor.shutdown();
        try {
            executor.awaitTermination(10, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

// Usage
// var processor = new ParallelStreamProcessor(4, 100);
// processor.process("input.log", "output.log", line -> {
//     if (line.contains("ERROR")) return null;
//     return line.toUpperCase();
// });
// processor.shutdown();
