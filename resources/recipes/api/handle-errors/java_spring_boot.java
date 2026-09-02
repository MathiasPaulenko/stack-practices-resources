import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import java.net.URI;
import java.util.Map;

@RestController
public class UserController {

    @GetMapping("/users/{userId}")
    public Map<String, Object> getUser(@PathVariable Long userId) {
        if (userId <= 0) {
            throw new ResponseStatusException(
                HttpStatus.NOT_FOUND,
                "No user with id " + userId
            );
        }
        return Map.of("id", userId, "name", "Ada");
    }

    @GetMapping("/crash")
    public Map<String, Object> crash() {
        throw new RuntimeException("Intentional crash for testing");
    }
}
