import net.jqwik.api.*;
import net.jqwik.api.stateful.*;

import java.util.List;
import java.util.Stack;

// Property-based testing examples with jqwik. Run with: mvn test
class PropertyBasedExamples {

    static String reverse(String s) {
        return new StringBuilder(s).reverse().toString();
    }

    @Property
    boolean reverseOfReverseIsOriginal(@ForAll String s) {
        return reverse(reverse(s)).equals(s);
    }

    @Property
    boolean concatenationLengthIsSum(
        @ForAll @StringLength(min = 0, max = 100) String a,
        @ForAll @StringLength(min = 0, max = 100) String b
    ) {
        return (a + b).length() == a.length() + b.length();
    }

    @Property
    boolean sortedListIsOrdered(@ForAll List<@IntRange(min = -1000, max = 1000) Integer> numbers) {
        List<Integer> sorted = numbers.stream().sorted().toList();
        for (int i = 1; i < sorted.size(); i++) {
            if (sorted.get(i - 1) > sorted.get(i)) return false;
        }
        return true;
    }

    // Custom arbitraries (generators)
    @Provide
    Arbitrary<Email> validEmails() {
        return Combinators.combine(
            Arbitraries.strings().alpha().ofLength(5),
            Arbitraries.of("gmail.com", "yahoo.com", "example.com")
        ).as((local, domain) -> new Email(local + "@" + domain));
    }

    @Property
    boolean emailParsingRoundTrip(@ForAll("validEmails") Email email) {
        return Email.parse(email.toString()).equals(email);
    }

    record Email(String value) {
        static Email parse(String s) {
            return new Email(s);
        }
    }

    // Stateful testing with ActionChain
    @Property
    void stackNeverCorrupts(@ForAll("stackActions") ActionChain<Stack<Integer>> chain) {
        chain.run();
    }

    @Provide
    ActionChainArbitrary<Stack<Integer>> stackActions() {
        return ActionChain.startWith(Stack::new)
            .withAction(pushActions())
            .withAction(new PopAction());
    }

    Arbitrary<Action<Stack<Integer>>> pushActions() {
        return Arbitraries.integers().between(-1000, 1000)
            .map(PushAction::new);
    }

    static class PushAction implements Action<Stack<Integer>> {
        private final int value;

        PushAction(int value) {
            this.value = value;
        }

        @Override
        public Stack<Integer> run(Stack<Integer> stack) {
            stack.push(value);
            return stack;
        }
    }

    static class PopAction implements Action<Stack<Integer>> {
        @Override
        public boolean precondition(Stack<Integer> stack) {
            return !stack.isEmpty();
        }

        @Override
        public Stack<Integer> run(Stack<Integer> stack) {
            stack.pop();
            return stack;
        }
    }
}
