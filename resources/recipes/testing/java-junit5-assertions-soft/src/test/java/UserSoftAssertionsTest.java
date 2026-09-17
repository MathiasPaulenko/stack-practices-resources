import static org.assertj.core.api.SoftAssertions.assertSoftly;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

import org.assertj.core.api.SoftAssertions;
import org.assertj.core.api.junit.jupiter.SoftAssertionsExtension;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.RegisterExtension;

/**
 * Runnable examples for "AssertJ Soft Assertions in JUnit5".
 * https://stackpractices.com/recipes/java-junit5-assertions-soft/
 *
 * The service collaborators are stubs so the tests compile and run
 * standalone — replace them with your real services.
 */
class UserSoftAssertionsTest {

    // ----- stubs (replace with your real services) -----

    record User(long id, String email, String role, boolean active, LocalDate createdAt) {}

    record OrderResponse(int statusCode, String orderId, BigDecimal total,
                         List<String> items, LocalDate estimatedDelivery) {}

    record Product(String name, BigDecimal price, String sku) {}

    record Config(int timeout, int retries, Map<String, String> featureFlags) {}

    record UserDto(long id, String name, String email, String role, boolean active, LocalDate createdAt) {}

    private User findUser() {
        return new User(1, "alice@example.com", "admin", true, LocalDate.of(2026, 1, 10));
    }

    // ----- 1. basic soft assertion: collect all failures, then assertAll() -----

    @Test
    void should_validate_all_user_fields() {
        User user = findUser();

        SoftAssertions softly = new SoftAssertions();
        softly.assertThat(user.id()).isEqualTo(1);
        softly.assertThat(user.email()).isEqualTo("alice@example.com");
        softly.assertThat(user.role()).isEqualTo("admin");
        softly.assertThat(user.active()).isTrue();
        softly.assertThat(user.createdAt()).isNotNull();
        softly.assertAll(); // without this call, failures are silently swallowed
    }

    // ----- 2. assertSoftly lambda: assertAll() is called for you -----

    @Test
    void should_validate_order_response() {
        OrderResponse response = new OrderResponse(
                201, "ord-99", new BigDecimal("99.99"),
                List.of("a", "b", "c"), LocalDate.now().plusDays(3));

        assertSoftly(softly -> {
            softly.assertThat(response.statusCode()).isEqualTo(201);
            softly.assertThat(response.orderId()).isNotNull();
            softly.assertThat(response.total()).isEqualByComparingTo("99.99");
            softly.assertThat(response.items()).hasSize(3);
            softly.assertThat(response.estimatedDelivery())
                    .isAfterOrEqualTo(LocalDate.now().plusDays(1));
        });
    }

    // ----- 3. soft assertions on collections -----

    @Test
    void should_validate_all_products() {
        List<Product> products = List.of(
                new Product("Widget", new BigDecimal("9.99"), "ABC-1234"),
                new Product("Gadget", new BigDecimal("19.99"), "DEF-5678"));

        SoftAssertions softly = new SoftAssertions();
        softly.assertThat(products).hasSize(2);

        for (Product p : products) {
            softly.assertThat(p.name()).isNotBlank();
            softly.assertThat(p.price()).isPositive();
            softly.assertThat(p.sku()).matches("^[A-Z]{3}-\\d{4}$");
        }
        softly.assertAll();
    }

    // ----- 4. custom .as() messages appear in the aggregated report -----

    @Test
    void should_validate_with_custom_messages() {
        Config config = new Config(45, 3, Map.of("monitoring", "on"));

        SoftAssertions softly = new SoftAssertions();
        softly.assertThat(config.timeout())
                .as("Production timeout must be at least 30s")
                .isGreaterThanOrEqualTo(30);
        softly.assertThat(config.retries())
                .as("Production retries must be between 1 and 5")
                .isBetween(1, 5);
        softly.assertThat(config.featureFlags())
                .as("Feature flags must include 'monitoring'")
                .containsKey("monitoring");
        softly.assertAll();
    }

    // ----- 5. field-by-field object comparison through the soft proxy -----

    @Test
    void should_validate_user_dto() {
        UserDto user = new UserDto(42, "Alice", "alice@example.com", "admin", true,
                LocalDate.now());
        UserDto expected = new UserDto(42, "Alice", "alice@example.com", "admin", true,
                LocalDate.of(2020, 1, 1));

        SoftAssertions softly = new SoftAssertions();
        softly.assertThat(user)
                .usingRecursiveComparison()
                .ignoringFields("createdAt")
                .isEqualTo(expected);
        softly.assertAll();
    }

    // ----- 6. @RegisterExtension: the extension calls assertAll() for you -----

    @RegisterExtension
    final SoftAssertionsExtension soft = new SoftAssertionsExtension();

    @Test
    void should_validate_with_extension(SoftAssertions softly) {
        User user = findUser();
        softly.assertThat(user.id()).isEqualTo(1);
        softly.assertThat(user.email()).contains("@");
        // no assertAll() needed — SoftAssertionsExtension runs it in afterTestExecution
    }

    // ----- 7. JUnit5 built-in assertAll for comparison -----

    @Test
    void should_validate_with_junit5_assert_all() {
        User user = findUser();

        org.junit.jupiter.api.Assertions.assertAll(
                () -> org.junit.jupiter.api.Assertions.assertEquals(1, user.id()),
                () -> org.junit.jupiter.api.Assertions.assertEquals("alice@example.com", user.email()),
                () -> org.junit.jupiter.api.Assertions.assertTrue(user.active()),
                () -> org.junit.jupiter.api.Assertions.assertEquals("admin", user.role())
        );
    }
}
