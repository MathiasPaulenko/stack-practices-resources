import jakarta.persistence.Entity;
import jakarta.persistence.EntityManager;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * Application-managed materialized view: a plain table rebuilt nightly by a
 * scheduled job. Companion code for
 * https://stackpractices.com/patterns/materialized-view-pattern/
 */
@Entity
@Table(name = "mv_product_stats")
class ProductStatsView {
    @Id
    private Long productId;
    private String productName;
    private Long totalSold;
    private BigDecimal totalRevenue;
    private Double averageRating;
    private LocalDate lastRefreshed;

    // getters...
}

@Service
public class ProductStatsRefreshService {

    private final EntityManager entityManager;

    public ProductStatsRefreshService(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    @Scheduled(cron = "0 0 2 * * ?") // Daily at 2 AM
    @Transactional
    public void refreshProductStats() {
        entityManager.createNativeQuery("""
            DROP TABLE IF EXISTS mv_product_stats;
            CREATE TABLE mv_product_stats AS
            SELECT
                p.id as product_id,
                p.name as product_name,
                COALESCE(SUM(oi.quantity), 0) as total_sold,
                COALESCE(SUM(oi.quantity * oi.price), 0) as total_revenue,
                COALESCE(AVG(r.rating), 0) as average_rating,
                CURRENT_DATE as last_refreshed
            FROM products p
            LEFT JOIN order_items oi ON p.id = oi.product_id
            LEFT JOIN reviews r ON p.id = r.product_id
            GROUP BY p.id, p.name;
            CREATE INDEX idx_mv_product ON mv_product_stats(product_id);
            """).executeUpdate();
    }
}

interface ProductStatsRepository extends JpaRepository<ProductStatsView, Long> {

    List<ProductStatsView> findByTotalSoldGreaterThan(Long minSold);

    @Query("SELECT p FROM ProductStatsView p ORDER BY p.totalRevenue DESC")
    List<ProductStatsView> findTopRevenue();
}
