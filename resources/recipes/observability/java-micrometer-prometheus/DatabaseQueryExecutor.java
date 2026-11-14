import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import java.util.List;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Service;

// Timer with manual start/stop. The Timer is a field — a Sample stops
// an already-registered timer, so no registry lookup happens per call.
// For outcome-dependent tags (status=success|error), keep two fields
// and stop the matching one: a Sample can't change the timer's tags.
@Service
public class DatabaseQueryExecutor {

    private final MeterRegistry registry;
    private final Timer dbQueryTimer;
    private final JdbcTemplate jdbcTemplate;
    private final RowMapper<Models.User> userRowMapper;

    public DatabaseQueryExecutor(MeterRegistry registry, JdbcTemplate jdbcTemplate,
                                 RowMapper<Models.User> userRowMapper) {
        this.registry = registry;
        this.jdbcTemplate = jdbcTemplate;
        this.userRowMapper = userRowMapper;
        this.dbQueryTimer = Timer.builder("db.query.duration")
            .tag("operation", "find_users")
            .register(registry);
    }

    public List<Models.User> findUsers(String query) {
        Timer.Sample sample = Timer.start(registry);
        try {
            return jdbcTemplate.query(query, userRowMapper);
        } finally {
            sample.stop(dbQueryTimer);
        }
    }
}
