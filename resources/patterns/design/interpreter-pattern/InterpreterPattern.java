import java.util.Map;

/**
 * Interpreter pattern: arithmetic expression language.
 * Compile: javac InterpreterPattern.java && java InterpreterPattern
 */
public class InterpreterPattern {

    public interface Expression {
        double interpret(Map<String, Double> context);
    }

    public static class NumberLiteral implements Expression {
        private final double value;
        public NumberLiteral(double value) { this.value = value; }
        public double interpret(Map<String, Double> context) { return value; }
    }

    public static class Variable implements Expression {
        private final String name;
        public Variable(String name) { this.name = name; }
        public double interpret(Map<String, Double> context) {
            return context.getOrDefault(name, 0.0);
        }
    }

    public static class Add implements Expression {
        private final Expression left, right;
        public Add(Expression left, Expression right) {
            this.left = left;
            this.right = right;
        }
        public double interpret(Map<String, Double> context) {
            return left.interpret(context) + right.interpret(context);
        }
    }

    public static class Subtract implements Expression {
        private final Expression left, right;
        public Subtract(Expression left, Expression right) {
            this.left = left;
            this.right = right;
        }
        public double interpret(Map<String, Double> context) {
            return left.interpret(context) - right.interpret(context);
        }
    }

    public static void main(String[] args) {
        // Evaluate "(10 + x) - 5" where x = 3
        Expression expr = new Subtract(
            new Add(new NumberLiteral(10), new Variable("x")),
            new NumberLiteral(5)
        );
        System.out.println(expr.interpret(Map.of("x", 3.0))); // 8.0
    }
}
