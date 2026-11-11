// Full-text search with the Elasticsearch 8 Java API Client.
// Dependencies (Maven):
//   co.elastic.clients:elasticsearch-java:8.x
//   com.fasterxml.jackson.core:jackson-databind
//   org.elasticsearch.client:elasticsearch-rest-client:8.x
// Requires a running Elasticsearch instance (see README for docker run).

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.json.JsonData;
import co.elastic.clients.json.jackson.JacksonJsonpMapper;
import co.elastic.clients.transport.rest_client.RestClientTransport;
import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;

import java.io.IOException;

public class ArticleSearch {
    private final ElasticsearchClient client;

    public ArticleSearch(RestClient restClient) {
        // RestHighLevelClient was removed in ES 8 — use the typed client
        this.client = new ElasticsearchClient(
            new RestClientTransport(restClient, new JacksonJsonpMapper()));
    }

    public SearchResponse<JsonData> search(String query) throws IOException {
        return client.search(s -> s
                .index("articles")
                .query(q -> q.multiMatch(m -> m
                        .query(query)
                        .fields("title^2", "content")
                        .fuzziness("AUTO")))
                .size(20),
            JsonData.class);
    }

    public static void main(String[] args) throws IOException {
        try (RestClient rest = RestClient.builder(new HttpHost("localhost", 9200)).build()) {
            ArticleSearch search = new ArticleSearch(rest);
            for (Hit<JsonData> hit : search.search("database optimiztion").hits().hits()) {
                System.out.println(hit.score() + "  " + hit.source());
            }
        }
    }
}
