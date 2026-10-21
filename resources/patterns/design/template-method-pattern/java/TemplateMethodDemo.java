import java.util.Map;

// Template Method Pattern — data import pipeline.
// The base class owns the algorithm skeleton (importData, final); subclasses
// implement only the steps that vary.
// Run with: javac TemplateMethodDemo.java && java TemplateMethodDemo

abstract class DataImporter {
    public final void importData(String source) {
        String raw = fetch(source);
        Map<String, Object> parsed = parse(raw);
        Map<String, Object> validated = validate(parsed);
        save(validated);
        onComplete();
    }

    protected abstract String fetch(String source);
    protected abstract Map<String, Object> parse(String raw);

    protected Map<String, Object> validate(Map<String, Object> data) {
        if (!data.containsKey("id")) {
            throw new IllegalArgumentException("Missing required field: id");
        }
        return data;
    }

    protected void save(Map<String, Object> data) {
        System.out.println("Saving: " + data);
    }

    // Named onComplete rather than notify: Object.notify() is final and any
    // method with that name will not compile.
    protected void onComplete() {
        // Hook — subclasses may override
    }
}

class CSVImporter extends DataImporter {
    protected String fetch(String source) {
        return "CSV content from " + source;
    }

    protected Map<String, Object> parse(String raw) {
        return Map.of("id", 1, "format", "csv", "content", raw);
    }
}

class JSONImporter extends DataImporter {
    protected String fetch(String source) {
        return "JSON content from " + source;
    }

    protected Map<String, Object> parse(String raw) {
        return Map.of("id", 2, "format", "json", "content", raw);
    }

    protected void onComplete() {
        System.out.println("JSON import completed!");
    }
}

public class TemplateMethodDemo {
    public static void main(String[] args) {
        new CSVImporter().importData("users.csv");
        new JSONImporter().importData("users.json");
    }
}
