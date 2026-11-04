import domain.Calculator;
import domain.EmailValidator;
import domain.Person;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.*;

class BasicParameterizedTest {

    private final Calculator calculator = new Calculator();
    private final EmailValidator validator = new EmailValidator();

    @ParameterizedTest
    @ValueSource(ints = {1, 2, 3, 4, 5})
    void testPositiveNumbers(int number) {
        assertTrue(number > 0);
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"  ", "\t"})
    void testBlankOrNullStrings(String input) {
        assertTrue(input == null || input.isBlank());
    }

    @ParameterizedTest(name = "[{index}] {0} + {1} = {2}")
    @CsvSource({"1, 1, 2", "2, 3, 5", "10, 20, 30", "-1, 1, 0", "0, 0, 0"})
    void testAddition(int a, int b, int expected) {
        assertEquals(expected, calculator.add(a, b));
    }

    @ParameterizedTest
    @CsvSource({"Alice, 30, true", "Bob, 17, false", "Charlie, 18, true", "Diana, 16, false"})
    void testAgeValidation(String name, int age, boolean canVote) {
        assertEquals(canVote, new Person(name, age).canVote());
    }

    static Stream<Arguments> provideEmails() {
        return Stream.of(
            Arguments.of("user@example.com", true),
            Arguments.of("admin@company.org", true),
            Arguments.of("not-an-email", false)
        );
    }

    @ParameterizedTest(name = "{0} validity = {1}")
    @MethodSource("provideEmails")
    void testEmailValidation(String email, boolean expected) {
        assertEquals(expected, validator.isValid(email));
    }
}
