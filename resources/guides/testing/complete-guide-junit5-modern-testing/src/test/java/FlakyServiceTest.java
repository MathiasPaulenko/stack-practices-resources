import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.assertTrue;

@ExtendWith(RetryExtension.class)
class FlakyServiceTest {

    private static int attempts = 0;

    @Test
    @DisplayName("should connect to external API")
    void testExternalApiConnection() {
        // Fails the first two attempts, succeeds on the third — shows retry works
        assertTrue(++attempts >= 3);
    }
}
