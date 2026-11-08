// Deep clone comparison: shallow copy vs manual deep copy in Java.
// Java has no structuredClone; the idiomatic deep clone is a copy
// constructor or copy method that recursively duplicates nested state.

import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

class Config {
    String name;
    Instant created;
    Set<String> tags;
    Map<String, Integer> nested;
    List<Config> children;

    Config(String name) {
        this.name = name;
        this.created = Instant.parse("2026-01-01T00:00:00Z");
        this.tags = new HashSet<>(Set.of("a", "b"));
        this.nested = new HashMap<>(Map.of("level", 2));
        this.children = new ArrayList<>();
    }

    // Deep copy constructor: every mutable field gets a fresh container.
    Config(Config other) {
        this.name = other.name;                       // immutable, share it
        this.created = other.created;                 // immutable, share it
        this.tags = new HashSet<>(other.tags);        // mutable: copy
        this.nested = new HashMap<>(other.nested);    // mutable: copy
        this.children = new ArrayList<>();
        for (Config child : other.children) {
            this.children.add(new Config(child));     // recursive deep copy
        }
    }
}

public class DeepClone {
    public static void main(String[] args) {
        Config original = new Config("config");
        original.children.add(new Config("child-1"));

        System.out.println("== shallow copy problem ==");
        Config shallow = original;
        shallow.nested.put("level", 99);
        System.out.println("shallow mutated original: " + (original.nested.get("level") == 99));

        original.nested.put("level", 2); // restore

        System.out.println("\n== deep copy constructor ==");
        Config deep = new Config(original);
        deep.nested.put("level", 42);
        deep.tags.add("c");
        deep.children.get(0).nested.put("level", 7);

        System.out.println("nested independent: " + (original.nested.get("level") == 2));
        System.out.println("tags independent: " + (original.tags.size() == 2));
        System.out.println("children deep-copied: " + (original.children.get(0).nested.get("level") == 2));
        System.out.println("containers are new objects: " + (deep.tags != original.tags));
    }
}
