import com.google.common.util.concurrent.RateLimiter;
import org.springframework.stereotype.Service;

@Service
public class ThrottledService {
    private final RateLimiter limiter = RateLimiter.create(10.0); // 10 permits/second

    public String processRequest(String request) {
        if (!limiter.tryAcquire()) {
            return "Rate limit exceeded — retry later";
        }
        return "Processed: " + request;
    }
}
