import org.springframework.ai.document.Document;
import org.springframework.ai.embedding.EmbeddingClient;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.pgvector.PgVectorStore;
import org.springframework.jdbc.core.JdbcTemplate;
import java.util.List;

public class SemanticSearchService {
    private final VectorStore vectorStore;

    public SemanticSearchService(EmbeddingClient embeddingClient, JdbcTemplate jdbc) {
        this.vectorStore = PgVectorStore.builder(jdbc, embeddingClient)
            .dimensions(1536)
            .distanceType(PgVectorStore.PgDistanceType.COSINE_DISTANCE)
            .initializeSchema(true)
            .build();
    }

    public void indexDocuments(List<String> texts) {
        List<Document> docs = texts.stream()
            .map(Document::new)
            .toList();
        vectorStore.add(docs);
    }

    public List<Document> search(String query, int topK) {
        return vectorStore.similaritySearch(
            SearchRequest.builder()
                .query(query)
                .topK(topK)
                .build()
        );
    }
}
