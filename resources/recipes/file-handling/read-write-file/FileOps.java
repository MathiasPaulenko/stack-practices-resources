import java.io.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.ArrayList;

// Safe file read/write utilities for Java (NIO).
// Compile: javac FileOps.java — Run: java FileOps
public class FileOps {

    // Atomic write: temp file + Files.move with ATOMIC_MOVE
    public static void atomicWrite(Path path, String content) throws IOException {
        Path parent = path.getParent();
        if (parent != null) Files.createDirectories(parent);
        Path tmp = Files.createTempFile(parent, path.getFileName().toString(), ".tmp");
        try {
            Files.writeString(tmp, content, StandardCharsets.UTF_8);
            Files.move(tmp, path, StandardCopyOption.ATOMIC_MOVE,
                       StandardCopyOption.REPLACE_EXISTING);
        } catch (Exception e) {
            Files.deleteIfExists(tmp);
            throw e;
        }
    }

    // Safe read with fallback
    public static String safeRead(Path path, String defaultValue) {
        if (!Files.exists(path)) return defaultValue;
        try {
            return Files.readString(path, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new UncheckedIOException("Failed to read " + path, e);
        }
    }

    // Read all lines
    public static List<String> readLines(Path path) throws IOException {
        return Files.readAllLines(path, StandardCharsets.UTF_8);
    }

    // Append a line
    public static void appendLine(Path path, String line) throws IOException {
        String entry = line + System.lineSeparator();
        Files.writeString(path, entry,
            StandardCharsets.UTF_8,
            StandardOpenOption.CREATE,
            StandardOpenOption.APPEND);
    }

    // Stream lines with try-with-resources
    public static void processLines(Path path, LineHandler handler) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
            String line;
            while ((line = reader.readLine()) != null) {
                handler.handle(line);
            }
        }
    }

    @FunctionalInterface
    public interface LineHandler {
        void handle(String line) throws IOException;
    }

    public static void main(String[] args) throws IOException {
        atomicWrite(Path.of("config.yaml"), "key: value\n");
        String config = safeRead(Path.of("config.yaml"), "key: default\n");
        processLines(Path.of("config.yaml"), line -> {
            if (line.contains("ERROR")) System.err.println(line);
        });
    }
}
