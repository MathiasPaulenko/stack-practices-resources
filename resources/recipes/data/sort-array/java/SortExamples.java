import java.util.*;
import java.util.stream.*;

public class SortExamples {
    record User(String name, int age) {}

    /** Multi-key sort: age first, ties broken alphabetically. */
    public static List<User> byAgeThenName(List<User> users) {
        return users.stream()
            .sorted(Comparator.comparingInt(User::age)
                              .thenComparing(User::name))
            .toList();
    }

    /** Sort with nulls pushed to the end. */
    public static List<Integer> nullsLast(List<Integer> values) {
        return values.stream()
            .sorted(Comparator.nullsLast(Comparator.naturalOrder()))
            .toList();
    }

    public static void main(String[] args) {
        var users = List.of(
            new User("Bob", 30), new User("Ada", 30), new User("Chen", 25));
        System.out.println(byAgeThenName(users));  // Chen, Ada, Bob
        System.out.println(nullsLast(Arrays.asList(3, null, 1)));  // [1, 3, null]
    }
}
