// Decorator Pattern simulation: coffee wrapped by milk, sugar, and whip
// decorators. Each decorator adds its own cost and label while delegating
// the rest of the call to the wrapped object.

interface Coffee {
    double cost();
    String description();
}

class SimpleCoffee implements Coffee {
    public double cost() { return 2.0; }
    public String description() { return "simple coffee"; }
}

// Base decorator: forwards everything it doesn't override.
abstract class CoffeeDecorator implements Coffee {
    protected final Coffee coffee;

    CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }

    public double cost() { return coffee.cost(); }
    public String description() { return coffee.description(); }
}

class MilkDecorator extends CoffeeDecorator {
    MilkDecorator(Coffee coffee) { super(coffee); }

    public double cost() { return super.cost() + 0.5; }
    public String description() { return super.description() + " + milk"; }
}

class SugarDecorator extends CoffeeDecorator {
    SugarDecorator(Coffee coffee) { super(coffee); }

    public double cost() { return super.cost() + 0.25; }
    public String description() { return super.description() + " + sugar"; }
}

class WhipDecorator extends CoffeeDecorator {
    WhipDecorator(Coffee coffee) { super(coffee); }

    public double cost() { return super.cost() + 0.75; }
    public String description() { return super.description() + " + whip"; }
}

public class DecoratorStack {
    static void show(Coffee coffee) {
        System.out.printf("%s -> $%.2f%n", coffee.description(), coffee.cost());
    }

    public static void main(String[] args) {
        System.out.println("== plain component ==");
        show(new SimpleCoffee());

        System.out.println("\n== stacked decorators (milk -> sugar -> whip) ==");
        show(new WhipDecorator(new SugarDecorator(new MilkDecorator(new SimpleCoffee()))));

        System.out.println("\n== same decorators, different order (whip -> milk -> sugar) ==");
        show(new SugarDecorator(new MilkDecorator(new WhipDecorator(new SimpleCoffee()))));

        System.out.println("\n== decorators compose freely: double milk, no whip ==");
        show(new MilkDecorator(new MilkDecorator(new SimpleCoffee())));
    }
}
