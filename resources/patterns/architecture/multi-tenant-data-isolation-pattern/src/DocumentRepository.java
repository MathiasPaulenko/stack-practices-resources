import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Map;

@Repository
public class DocumentRepository {

    private final JdbcTemplate jdbc;

    public DocumentRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<Map<String, Object>> findAll() {
        String tenant = TenantContext.getTenantId();
        // The header is attacker-controlled input. A raw concatenation here
        // is SQL injection — validate the schema name before interpolating.
        if (!tenant.matches("[a-z0-9_]{1,32}")) {
            throw new IllegalArgumentException("Invalid tenant id");
        }
        return jdbc.queryForList(
            "SELECT id, title, content FROM tenant_" + tenant + ".documents"
        );
    }
}
