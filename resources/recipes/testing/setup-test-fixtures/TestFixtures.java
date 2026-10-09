import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.*;

/**
 * JUnit 5 fixture lifecycle: @BeforeAll/@AfterAll once per class,
 * @BeforeEach per test, factory methods, @ParameterizedTest inputs.
 *
 * Dependencies: junit-jupiter (Maven/Gradle test scope).
 * Run: mvn test or your IDE's JUnit runner.
 */
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class TestFixtures {

    static class User {
        final String role;
        User(String role) { this.role = role; }
        boolean canDelete() { return "admin".equals(role); }
    }

    private StringBuilder sharedLog;

    @BeforeAll
    void suiteSetup() {
        sharedLog = new StringBuilder("suite;");
    }

    @BeforeEach
    void resetPerTest() {
        sharedLog.append("test;");
    }

    // Factory method: deterministic object per call
    private User user(String role) {
        return new User(role);
    }

    @Test
    @DisplayName("admin can delete")
    void adminCanDelete() {
        assertTrue(user("admin").canDelete());
    }

    @ParameterizedTest
    @CsvSource({
        "admin, true",
        "editor, false",
        "viewer, false"
    })
    void onlyAdminCanDelete(String role, boolean expected) {
        assertEquals(expected, user(role).canDelete());
    }

    @Test
    void sharedStateResetsCleanly() {
        assertTrue(sharedLog.toString().startsWith("suite;"));
    }
}
