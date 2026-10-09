import net.datafaker.Faker;
import java.util.List;
import java.util.stream.IntStream;

/**
 * Deterministic test data generators with DataFaker (+ Instancio for
 * type-aware object graphs).
 *
 * Dependencies (Maven):
 *   net.datafaker:datafaker:2.x
 *   org.instancio:instancio-junit:5.x (optional)
 */
public class TestDataGenerator {
    private static final Faker faker = new Faker();

    public static User createUser() {
        return User.builder()
            .id(faker.number().randomNumber())
            .name(faker.name().fullName())
            .email(faker.internet().emailAddress())
            .age(faker.number().numberBetween(18, 90))
            .isActive(true)
            .build();
    }

    public static List<User> createUsers(int count) {
        return IntStream.range(0, count)
            .mapToObj(i -> createUser())
            .toList();
    }

    /** JUnit 5 @MethodSource provider for parameterized tests. */
    public static java.util.stream.Stream<org.junit.jupiter.params.provider.Arguments> emailProvider() {
        return java.util.stream.Stream
            .generate(() -> org.junit.jupiter.params.provider.Arguments.of(faker.internet().emailAddress()))
            .limit(50);
    }

    public static void main(String[] args) {
        System.out.println("user: " + createUser());
        System.out.println("batch size: " + createUsers(5).size());
    }
}

// Type-aware generation alternative (requires instancio):
//
//   User user = Instancio.of(User.class)
//       .set(Select.field("role"), "admin")
//       .generate(Select.field("age"), gen -> gen.ints().range(18, 90))
//       .create();
//   List<User> users = Instancio.ofList(User.class).size(100).create();
