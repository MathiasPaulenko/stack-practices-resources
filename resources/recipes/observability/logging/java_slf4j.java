import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;

/**
 * Structured logging with SLF4J + Logback: parameterized messages and MDC
 * correlation IDs. Add %X{requestId} to the Logback encoder pattern so the
 * correlation ID prints on every line.
 *
 * Run: mvn compile exec:java -Dexec.mainClass=UserService
 */
public class UserService {
    private static final Logger log = LoggerFactory.getLogger(UserService.class);

    // Stand-in for whatever your web framework exposes (filter, interceptor, etc.)
    static final class RequestContext {
        static String currentRequestId() {
            return "abc-123";
        }
    }

    public void login(String userId) {
        MDC.put("requestId", RequestContext.currentRequestId());
        try {
            log.debug("Processing user {}", userId);
            log.info("User {} logged in", userId);
            throw new RuntimeException("database timeout");
        } catch (Exception e) {
            log.error("Login failed for user {}", userId, e);
        } finally {
            MDC.clear();
        }
    }

    public static void main(String[] args) {
        new UserService().login("u-42");
    }
}
