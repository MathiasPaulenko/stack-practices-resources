// Recursive JSON diff over a Jackson tree — no third-party diff library.
// Compile:  javac -cp "jackson-databind.jar;jackson-core.jar;jackson-annotations.jar" JsonDiff.java
// Run:      java -cp ".;jackson-databind.jar;jackson-core.jar;jackson-annotations.jar" JsonDiff old.json new.json

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.util.LinkedHashMap;
import java.util.Map;

public class JsonDiff {

    public static Map<String, Object[]> diff(JsonNode a, JsonNode b,
                                             String path, Map<String, Object[]> out) {
        if (a.equals(b)) return out;

        if (a.isObject() && b.isObject()) {
            a.fields().forEachRemaining(e -> {
                JsonNode av = e.getValue();
                JsonNode bv = b.get(e.getKey());
                if (bv == null) out.put(path + "/" + e.getKey(), new Object[]{av, null});
                else diff(av, bv, path + "/" + e.getKey(), out);
            });
            b.fields().forEachRemaining(e -> {
                if (a.get(e.getKey()) == null)
                    out.put(path + "/" + e.getKey(), new Object[]{null, e.getValue()});
            });
        } else if (a.isArray() && b.isArray()) {
            int common = Math.min(a.size(), b.size());
            for (int i = 0; i < common; i++) diff(a.get(i), b.get(i), path + "[" + i + "]", out);
            for (int i = common; i < a.size(); i++) out.put(path + "[" + i + "]", new Object[]{a.get(i), null});
            for (int i = common; i < b.size(); i++) out.put(path + "[" + i + "]", new Object[]{null, b.get(i)});
        } else {
            out.put(path.isEmpty() ? "/" : path, new Object[]{a, b});
        }
        return out;
    }

    public static void main(String[] args) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode oldNode = mapper.readTree(new File(args[0]));
        JsonNode newNode = mapper.readTree(new File(args[1]));

        Map<String, Object[]> diff = diff(oldNode, newNode, "", new LinkedHashMap<>());
        if (diff.isEmpty()) {
            System.out.println("No differences found.");
            return;
        }
        diff.forEach((path, pair) ->
            System.out.printf("%-30s -> %s => %s%n", path, pair[0], pair[1]));
    }
}
