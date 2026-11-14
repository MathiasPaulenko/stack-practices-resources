import io.micrometer.core.annotation.Counted;
import io.micrometer.core.annotation.Timed;
import java.util.List;
import org.springframework.stereotype.Service;

// @Counted and @Timed — annotation-driven metrics.
// @Timed works out of the box (Spring Boot auto-configures TimedAspect);
// @Counted needs the CountedAspect bean declared in MetricsConfig.
@Service
public class UserService {

    @Counted(value = "users.searched", description = "Total user searches")
    @Timed(value = "users.search.duration", description = "User search time",
           percentiles = {0.5, 0.95, 0.99})
    public List<Models.User> searchUsers(String query) {
        // ... search logic ...
        return List.of();
    }
}
