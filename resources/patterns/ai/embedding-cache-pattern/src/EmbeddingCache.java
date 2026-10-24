import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.*;

public class EmbeddingCache {

    record CacheEntry(List<Double> embedding, String model, long createdAt) {}

    private final Map<String, CacheEntry> cache = new HashMap<>();
    private final long ttlSeconds;
    private int hits = 0;
    private int misses = 0;

    public EmbeddingCache(long ttlSeconds) {
        this.ttlSeconds = ttlSeconds;
    }

    public EmbeddingCache() {
        this(86400L * 30);
    }

    private String makeKey(String text, String model) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest(text.getBytes(StandardCharsets.UTF_8));
        StringBuilder hex = new StringBuilder();
        for (byte b : hash) hex.append(String.format("%02x", b));
        return model + ":" + hex;
    }

    public Optional<List<Double>> get(String text, String model) throws Exception {
        String key = makeKey(text, model);
        CacheEntry entry = cache.get(key);

        if (entry == null) {
            misses++;
            return Optional.empty();
        }

        if (System.currentTimeMillis() / 1000 - entry.createdAt() > ttlSeconds) {
            cache.remove(key);
            misses++;
            return Optional.empty();
        }

        hits++;
        return Optional.of(entry.embedding());
    }

    public void set(String text, String model, List<Double> embedding) throws Exception {
        String key = makeKey(text, model);
        cache.put(key, new CacheEntry(embedding, model, System.currentTimeMillis() / 1000));
    }

    public List<Double> getOrCompute(String text, String model,
                                      java.util.function.BiFunction<String, String, List<Double>> embedFn) throws Exception {
        Optional<List<Double>> cached = get(text, model);
        if (cached.isPresent()) return cached.get();

        List<Double> embedding = embedFn.apply(text, model);
        set(text, model, embedding);
        return embedding;
    }

    public Map<String, Object> stats() {
        return Map.of(
            "hits", hits,
            "misses", misses,
            "size", cache.size(),
            "hitRate", hits / (double) Math.max(hits + misses, 1)
        );
    }

    public int invalidateModel(String model) {
        Set<String> keys = new HashSet<>();
        for (String key : cache.keySet()) {
            if (key.startsWith(model + ":")) keys.add(key);
        }
        keys.forEach(cache::remove);
        return keys.size();
    }

    public static void main(String[] args) throws Exception {
        var cache = new EmbeddingCache(3600);

        var embedFn = (java.util.function.BiFunction<String, String, List<Double>>) (text, model) -> {
            System.out.printf("  [API CALL] Embedding '%s...' with %s%n", text.substring(0, Math.min(30, text.length())), model);
            return List.of(text.length() * 0.01, (double) (text.hashCode() % 100) / 100, 0.5);
        };

        var documents = List.of(
            "Python async programming guide",
            "JavaScript event loop explained",
            "Python async programming guide",
            "Database indexing strategies",
            "JavaScript event loop explained"
        );

        System.out.println("=== Single embeddings ===");
        for (String doc : documents) {
            var emb = cache.getOrCompute(doc, "text-embedding-3-small", embedFn);
            System.out.printf("  Result: [%.4f, %.4f, ...]%n", emb.get(0), emb.get(1));
        }

        System.out.printf("%nCache stats: %s%n", cache.stats());

        System.out.printf("%n=== Model invalidation ===%n");
        int removed = cache.invalidateModel("text-embedding-3-small");
        System.out.printf("Removed %d entries%n", removed);
        System.out.printf("Cache stats: %s%n", cache.stats());
    }
}
