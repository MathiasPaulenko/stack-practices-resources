import java.util.*;

public class HybridSearch {

    record Document(String id, String text) {}
    record SearchResult(String id, double score) {}

    public static List<SearchResult> bm25Search(
            String query, List<Document> documents, int topK) {
        String[] queryTerms = query.toLowerCase().split(" ");
        Map<String, Double> scores = new HashMap<>();
        int docCount = documents.size();
        double avgLen = documents.stream()
                .mapToInt(d -> d.text().split(" ").length)
                .average().orElse(1);
        double k1 = 1.5, b = 0.75;

        for (Document doc : documents) {
            String[] docTerms = doc.text().toLowerCase().split(" ");
            int docLen = docTerms.length;
            double score = 0;

            for (String term : queryTerms) {
                long tf = Arrays.stream(docTerms).filter(t -> t.equals(term)).count();
                long df = documents.stream()
                        .filter(d -> d.text().toLowerCase().contains(term))
                        .count();
                double idf = Math.log((docCount - df + 0.5) / (df + 0.5) + 1);
                score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * docLen / avgLen));
            }

            if (score > 0) scores.put(doc.id(), score);
        }

        return scores.entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
                .limit(topK)
                .map(e -> new SearchResult(e.getKey(), e.getValue()))
                .toList();
    }

    public static List<SearchResult> vectorSearch(
            double[] queryEmb, Map<String, double[]> docEmbs, int topK) {
        Map<String, Double> scores = new HashMap<>();

        for (var entry : docEmbs.entrySet()) {
            scores.put(entry.getKey(), cosine(queryEmb, entry.getValue()));
        }

        return scores.entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
                .limit(topK)
                .map(e -> new SearchResult(e.getKey(), e.getValue()))
                .toList();
    }

    static double cosine(double[] a, double[] b) {
        double dot = 0, normA = 0, normB = 0;
        for (int i = 0; i < a.length; i++) {
            dot += a[i] * b[i];
            normA += a[i] * a[i];
            normB += b[i] * b[i];
        }
        return dot / (Math.sqrt(normA) * Math.sqrt(normB) + 1e-10);
    }

    public static List<SearchResult> reciprocalRankFusion(
            List<List<SearchResult>> resultLists, int k, int topK) {
        Map<String, Double> fused = new HashMap<>();

        for (List<SearchResult> results : resultLists) {
            for (int rank = 0; rank < results.size(); rank++) {
                String id = results.get(rank).id();
                fused.merge(id, 1.0 / (k + rank + 1), Double::sum);
            }
        }

        return fused.entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
                .limit(topK)
                .map(e -> new SearchResult(e.getKey(), e.getValue()))
                .toList();
    }

    public static void main(String[] args) {
        var docs = List.of(
            new Document("d1", "Python async programming with asyncio"),
            new Document("d2", "JavaScript event loop and promises"),
            new Document("d3", "Concurrent task execution in Python"),
            new Document("d4", "Node.js worker threads for CPU tasks")
        );

        var bm25Results = bm25Search("python async tasks", docs, 5);
        var vectorResults = vectorSearch(
            new double[]{0.12, 0.85, 0.33, 0.41},
            Map.of(
                "d1", new double[]{0.11, 0.82, 0.30, 0.45},
                "d2", new double[]{0.05, 0.20, 0.71, 0.10},
                "d3", new double[]{0.13, 0.79, 0.35, 0.38},
                "d4", new double[]{0.02, 0.15, 0.60, 0.05}
            ),
            5
        );

        var hybrid = reciprocalRankFusion(
            List.of(bm25Results, vectorResults), 60, 5);
        hybrid.forEach(r -> System.out.printf("%s: %.4f%n", r.id(), r.score()));
    }
}
