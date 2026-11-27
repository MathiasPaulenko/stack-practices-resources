import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

import javax.sql.DataSource;
import java.util.List;
import java.util.Map;

/**
 * Range-based sharding: contiguous ID ranges map to dedicated DataSources.
 * Cheap range scans, but a hot range concentrates load on one node.
 */
@Component
public class RangeShardRouter {

    private final List<DataSource> shards;
    private final List<Long> rangeBoundaries;

    // Shard 0: IDs 1-1,000,000
    // Shard 1: IDs 1,000,001-2,000,000
    // Shard 2: IDs 2,000,001+
    public RangeShardRouter(List<DataSource> shards, List<Long> boundaries) {
        this.shards = shards;
        this.rangeBoundaries = boundaries;
    }

    public JdbcTemplate getShardForId(Long id) {
        int shardIndex = 0;
        for (Long boundary : rangeBoundaries) {
            if (id <= boundary) break;
            shardIndex++;
        }
        return new JdbcTemplate(shards.get(shardIndex));
    }

    public void insertOrder(Long orderId, Long customerId, Double amount) {
        JdbcTemplate shard = getShardForId(orderId);
        shard.update(
            "INSERT INTO orders (id, customer_id, amount) VALUES (?, ?, ?)",
            orderId, customerId, amount
        );
    }

    public Map<String, Object> getOrder(Long orderId) {
        JdbcTemplate shard = getShardForId(orderId);
        return shard.queryForMap(
            "SELECT * FROM orders WHERE id = ?",
            orderId
        );
    }
}
