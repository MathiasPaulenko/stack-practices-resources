import domain.Calculator;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.DynamicTest.dynamicTest;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

class DynamicTestsTest {

    private final Calculator calculator = new Calculator();

    @TestFactory
    Stream<DynamicTest> testStringOperations() {
        Map<String, String> expected = Map.of(
            "hello", "HELLO",
            "world", "WORLD",
            "java", "JAVA"
        );

        return expected.entrySet().stream()
            .map(e -> dynamicTest(
                "uppercase: " + e.getKey(),
                () -> assertEquals(e.getValue(), e.getKey().toUpperCase())
            ));
    }

    @TestFactory
    List<DynamicTest> testMultipleScenarios() {
        return List.of(
            dynamicTest("add positive numbers", () -> assertEquals(5, calculator.add(2, 3))),
            dynamicTest("add negative numbers", () -> assertEquals(-5, calculator.add(-2, -3))),
            dynamicTest("add zero", () -> assertEquals(5, calculator.add(5, 0)))
        );
    }
}
