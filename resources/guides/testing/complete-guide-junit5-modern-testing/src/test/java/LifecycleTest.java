import org.junit.jupiter.api.*;

class LifecycleTest {

    @BeforeAll
    static void setUpAll() {
        // Runs once before all tests in the class
    }

    @BeforeEach
    void setUp() {
        // Runs before each test
    }

    @Test
    void firstTest() {
        Assertions.assertTrue(true);
    }

    @Test
    void secondTest() {
        Assertions.assertTrue(true);
    }

    @AfterEach
    void tearDown() {
        // Runs after each test
    }

    @AfterAll
    static void tearDownAll() {
        // Runs once after all tests in the class
    }
}
