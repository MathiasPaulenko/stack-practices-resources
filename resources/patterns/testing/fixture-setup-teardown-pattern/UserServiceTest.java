// Java — JUnit 5 setup/teardown lifecycle
// Run: mvn test (requires junit-jupiter on the classpath)
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class UserServiceTest {

    private UserService service;
    private FakeUserRepository repo;

    @BeforeEach
    void setUp() {
        // Runs before each test — fresh repository and service
        repo = new FakeUserRepository();
        service = new UserService(repo);
        service.createUser("Alice", "alice@x.com");
    }

    @AfterEach
    void tearDown() {
        // Runs after each test, even on failure
        repo.clear();
        service = null;
    }

    @BeforeAll
    static void setUpAll() {
        // Runs once before all tests in the class
        System.setProperty("TEST_MODE", "true");
    }

    @AfterAll
    static void tearDownAll() {
        // Runs once after all tests in the class
        System.clearProperty("TEST_MODE");
    }

    @Test
    void testFindUser() {
        User user = service.findByEmail("alice@x.com");
        assertEquals("Alice", user.getName());
    }

    @Test
    void testDuplicateEmail() {
        assertThrows(DuplicateEmailException.class, () -> {
            service.createUser("Bob", "alice@x.com");
        });
    }
}
