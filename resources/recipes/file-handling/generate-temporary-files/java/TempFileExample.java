import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;
import java.util.stream.Stream;

/**
 * Temporary file and directory patterns from the Generate Temporary Files recipe.
 *
 * Run: javac TempFileExample.java && java TempFileExample
 */
public class TempFileExample {
    public static void main(String[] args) throws IOException {
        // Create temp file in the default temp directory
        Path tempFile = Files.createTempFile("prefix-", ".txt");
        System.out.println("Created: " + tempFile);
        Files.writeString(tempFile, "temporary data");

        // Create temp directory
        Path tempDir = Files.createTempDirectory("myapp-");
        Path nested = tempDir.resolve("nested.txt");
        Files.writeString(nested, "nested content");

        // deleteOnExit deletes in reverse registration order, and a directory
        // must be empty to go — register the parent first so children are
        // removed before it. Best effort only: nothing fires on a JVM crash.
        tempDir.toFile().deleteOnExit();
        nested.toFile().deleteOnExit();
        tempFile.toFile().deleteOnExit();

        // Explicit cleanup. Files.walk holds a directory handle, so it must
        // be closed — try-with-resources or the stream leaks descriptors.
        Files.deleteIfExists(tempFile);
        try (Stream<Path> paths = Files.walk(tempDir)) {
            paths.sorted(Comparator.reverseOrder())
                .forEach(p -> {
                    try {
                        Files.deleteIfExists(p);
                    } catch (IOException e) {
                        // best effort: the sweep continues
                    }
                });
        }
        System.out.println("tempDir removed: " + !Files.exists(tempDir));
    }
}
