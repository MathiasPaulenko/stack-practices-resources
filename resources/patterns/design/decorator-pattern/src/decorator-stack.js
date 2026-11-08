// Decorator Pattern simulation: coffee wrapped by milk, sugar, and whip decorators.
// Each decorator adds its own cost and label while delegating the rest of the
// call to the wrapped object.

class Coffee {
  cost() {
    return 2.0;
  }

  description() {
    return "simple coffee";
  }
}

// Base decorator: forwards everything it doesn't override.
class CoffeeDecorator {
  constructor(coffee) {
    this.coffee = coffee;
  }

  cost() {
    return this.coffee.cost();
  }

  description() {
    return this.coffee.description();
  }
}

class MilkDecorator extends CoffeeDecorator {
  cost() {
    return super.cost() + 0.5;
  }

  description() {
    return `${super.description()} + milk`;
  }
}

class SugarDecorator extends CoffeeDecorator {
  cost() {
    return super.cost() + 0.25;
  }

  description() {
    return `${super.description()} + sugar`;
  }
}

class WhipDecorator extends CoffeeDecorator {
  cost() {
    return super.cost() + 0.75;
  }

  description() {
    return `${super.description()} + whip`;
  }
}

function show(coffee) {
  console.log(`${coffee.description()} -> $${coffee.cost().toFixed(2)}`);
}

console.log("== plain component ==");
show(new Coffee());

console.log("\n== stacked decorators (milk -> sugar -> whip) ==");
show(new WhipDecorator(new SugarDecorator(new MilkDecorator(new Coffee()))));

console.log("\n== same decorators, different order (whip -> milk -> sugar) ==");
show(new SugarDecorator(new MilkDecorator(new WhipDecorator(new Coffee()))));

console.log("\n== decorators compose freely: double milk, no whip ==");
show(new MilkDecorator(new MilkDecorator(new Coffee())));
