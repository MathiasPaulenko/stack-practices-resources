import domain.Calculator;
import org.junit.jupiter.api.Test;
import java.time.Duration;
import static org.junit.jupiter.api.Assertions.*;

class BasicAssertionsTest {

    private final Calculator calculator = new Calculator();

    @Test
    void testBasicAssertions() {
        assertEquals(4, 2 + 2);
        assertNotEquals(5, 2 + 2);
        assertTrue(5 > 3);
        assertFalse(5 < 3);
        assertNull(null);
        assertNotNull(new Object());
    }

    @Test
    void testWithMessage() {
        assertEquals(4, calculator.add(2, 2), "2 + 2 should equal 4");
        assertEquals(4, calculator.add(2, 2), () -> "Calculation failed at runtime");
    }

    @Test
    void testGroupedAssertions() {
        assertAll("calculator",
            () -> assertEquals(4, calculator.add(2, 2)),
            () -> assertEquals(0, calculator.add(0, 0)),
            () -> assertEquals(-1, calculator.add(-3, 2))
        );
    }

    @Test
    void testExceptions() {
        IllegalStateException ex = assertThrows(
            IllegalStateException.class,
            () -> { throw new IllegalStateException("Order cannot be processed"); }
        );
        assertEquals("Order cannot be processed", ex.getMessage());
    }

    @Test
    void testTimeout() {
        assertTimeout(Duration.ofSeconds(2), () -> calculator.add(1, 1));
        assertTimeoutPreemptively(Duration.ofMillis(500), () -> calculator.add(2, 2));
    }
}
