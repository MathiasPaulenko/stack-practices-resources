// Jackson recursive merge. Maven: com.fasterxml.jackson.core:jackson-databind
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import java.io.File;

public class JsonMerge {
    private static final ObjectMapper mapper = new ObjectMapper();

    public static JsonNode merge(JsonNode base, JsonNode override) {
        if (base.isArray() && override.isArray()) {
            ArrayNode merged = mapper.createArrayNode();
            merged.addAll((ArrayNode) base);
            merged.addAll((ArrayNode) override);
            return merged;
        } else if (base.isObject() && override.isObject()) {
            ObjectNode merged = ((ObjectNode) base).deepCopy();
            override.fields().forEachRemaining(e -> {
                JsonNode existing = merged.get(e.getKey());
                if (existing != null && existing.isObject() && e.getValue().isObject()) {
                    merged.set(e.getKey(), merge(existing, e.getValue()));
                } else {
                    merged.set(e.getKey(), e.getValue());
                }
            });
            return merged;
        }
        return override;
    }

    public static void main(String[] args) throws Exception {
        JsonNode base = mapper.readTree(new File("base.json"));
        JsonNode override = mapper.readTree(new File("override.json"));
        System.out.println(merge(base, override).toPrettyString());
    }
}
