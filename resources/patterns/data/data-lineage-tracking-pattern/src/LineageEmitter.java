// LineageEmitter.java — emit lineage events from Java pipelines
// Requires Jackson on the classpath. Posts raw OpenLineage JSON to Marquez.
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.UUID;
import java.time.Instant;

public class LineageEmitter {
    private static final String MARQUEZ_URL = "http://marquez:5000";
    private final HttpClient client = HttpClient.newHttpClient();
    private final ObjectMapper mapper = new ObjectMapper();

    public void emitRun(String jobName, String runId, String eventType,
                        String[] inputTables, String[] outputTables) {
        try {
            var event = mapper.createObjectNode();
            event.put("eventType", eventType);
            event.put("eventTime", Instant.now().toString());
            event.put("producer", "https://github.com/shop/data-pipelines/tree/main/LineageEmitter");

            var run = mapper.createObjectNode();
            run.put("runId", runId);
            event.set("run", run);

            var job = mapper.createObjectNode();
            job.put("namespace", "shop");
            job.put("name", jobName);
            event.set("job", job);

            var inputs = mapper.createArrayNode();
            for (String table : inputTables) {
                var ds = mapper.createObjectNode();
                ds.put("namespace", "postgres://source");
                ds.put("name", table);
                inputs.add(ds);
            }
            event.set("inputs", inputs);

            var outputs = mapper.createArrayNode();
            for (String table : outputTables) {
                var ds = mapper.createObjectNode();
                ds.put("namespace", "postgres://warehouse");
                ds.put("name", table);
                outputs.add(ds);
            }
            event.set("outputs", outputs);

            var request = HttpRequest.newBuilder()
                .uri(URI.create(MARQUEZ_URL + "/api/v1/lineage"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(event)))
                .build();

            client.send(request, HttpResponse.BodyHandlers.ofString());
        } catch (Exception e) {
            throw new RuntimeException("Failed to emit lineage event", e);
        }
    }
}
