import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LogParser {
    private static final Pattern LOG_PATTERN = Pattern.compile(
        "^(\\S+) \\S+ \\S+ \\[(\\d{2}/\\w{3}/\\d{4}:\\d{2}:\\d{2}:\\d{2} [+-]\\d{4})\\] " +
        "\\\"(\\S+) (\\S+) ([^\"]+)\\\" (\\d{3}) (\\S+)"
    );

    public static void main(String[] args) throws IOException {
        Map<String, Integer> statusCounts = new HashMap<>();
        int total = 0;
        int parseErrors = 0;

        try (BufferedReader br = new BufferedReader(new FileReader("access.log"))) {
            String line;
            while ((line = br.readLine()) != null) {
                total++;
                Matcher m = LOG_PATTERN.matcher(line);
                if (m.find()) {
                    String status = m.group(6);
                    statusCounts.put(status, statusCounts.getOrDefault(status, 0) + 1);
                } else {
                    parseErrors++;
                    System.out.println("malformed line " + total + ": " + line.substring(0, Math.min(line.length(), 120)));
                }
            }
        }

        System.out.println("\nStatus counts: " + statusCounts);
        System.out.printf("Parse errors: %d/%d (%.2f%%)%n", parseErrors, total, 100.0 * parseErrors / total);
    }
}
