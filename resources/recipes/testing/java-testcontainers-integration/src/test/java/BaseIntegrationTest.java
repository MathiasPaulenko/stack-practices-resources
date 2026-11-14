import org.testcontainers.containers.PostgreSQLContainer;

/**
 * Shared container pattern: one Postgres instance for every subclass.
 * Extend this class instead of declaring your own container.
 */
public abstract class BaseIntegrationTest {

    static final PostgreSQLContainer<?> SHARED_POSTGRES;

    static {
        SHARED_POSTGRES = new PostgreSQLContainer<>("postgres:16-alpine")
            .withDatabaseName("testdb")
            .withReuse(true);
        SHARED_POSTGRES.start();
    }

    protected String getJdbcUrl() {
        return SHARED_POSTGRES.getJdbcUrl();
    }
}
