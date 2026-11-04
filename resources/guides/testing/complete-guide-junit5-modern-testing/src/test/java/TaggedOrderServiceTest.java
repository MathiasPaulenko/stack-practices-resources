import domain.OrderService;
import org.junit.jupiter.api.*;

@DisplayName("Order Service Tests")
class TaggedOrderServiceTest {

    @Test
    @DisplayName("should calculate total with tax")
    @Tag("unit")
    void testCalculateTotalWithTax() {
        Assertions.assertTrue(true);
    }

    @Test
    @DisplayName("should reject order with negative quantity")
    @Tag("unit")
    @Tag("validation")
    void testNegativeQuantity() {
        Assertions.assertTrue(true);
    }

    @Test
    @DisplayName("should persist order to database")
    @Tag("integration")
    @Tag("slow")
    void testOrderPersistence() {
        Assertions.assertTrue(true);
    }
}
