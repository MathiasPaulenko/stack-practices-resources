import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public interface ComparableContract<T extends Comparable<T>> {

    T createSmallerValue();
    T createLargerValue();

    @Test
    @DisplayName("returns positive when comparing smaller to larger")
    default void returnsPositiveWhenSmallerComparedToLarger() {
        assertTrue(createSmallerValue().compareTo(createLargerValue()) < 0);
    }

    @Test
    @DisplayName("returns negative when comparing larger to smaller")
    default void returnsNegativeWhenLargerComparedToSmaller() {
        assertTrue(createLargerValue().compareTo(createSmallerValue()) > 0);
    }

    @Test
    @DisplayName("returns zero when comparing to self")
    default void returnsZeroWhenComparedToSelf() {
        T value = createSmallerValue();
        assertEquals(0, value.compareTo(value));
    }
}
