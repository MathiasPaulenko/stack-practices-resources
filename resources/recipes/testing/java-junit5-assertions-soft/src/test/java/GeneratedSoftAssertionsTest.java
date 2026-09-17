import domain.SoftAssertions;
import domain.User;
import org.junit.jupiter.api.Test;

/**
 * Demonstrates the assertj-assertions-generator-maven-plugin: it reads the
 * domain.User POJO and generates domain.SoftAssertions — an entry point that
 * extends org.assertj.core.api.SoftAssertions and adds a typed
 * assertThat(User) returning a generated UserAssert with hasXxx() methods.
 *
 * The generated classes land in target/generated-test-sources/assertj-assertions
 * during the generate-test-sources phase, so `mvn test` builds them automatically.
 */
class GeneratedSoftAssertionsTest {

    @Test
    void should_validate_user_with_generated_soft_assertions() {
        User user = new User(1, "alice@example.com", "admin", true);

        SoftAssertions softly = new SoftAssertions();
        softly.assertThat(user)
                .hasId(1)
                .hasEmail("alice@example.com")
                .hasRole("admin")
                .isActive();
        softly.assertAll();
    }

    @Test
    void generated_entry_point_still_supports_standard_assertions() {
        User user = new User(2, "bob@example.com", "user", false);

        SoftAssertions softly = new SoftAssertions();
        // generated typed assertion for User
        softly.assertThat(user).hasRole("user");
        // inherited standard assertThat overloads still work
        softly.assertThat(user.getEmail()).contains("@");
        softly.assertThat(user.getId()).isPositive();
        softly.assertAll();
    }
}
