import java.io.*;
import java.nio.file.*;

public class StreamProcessor {
    public static void process(String input, String output) throws IOException {
        try (BufferedReader r = Files.newBufferedReader(Path.of(input));
             BufferedWriter w = Files.newBufferedWriter(Path.of(output))) {
            String line;
            while ((line = r.readLine()) != null) {
                w.write(line.toUpperCase());
                w.newLine();
            }
        }
    }
}
