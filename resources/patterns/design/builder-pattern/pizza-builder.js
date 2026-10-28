// Fluent Builder for a Pizza object, including a toBuilder() copy method.

class Pizza {
  constructor(size, cheese, pepperoni, mushrooms) {
    this.size = size;
    this.cheese = cheese;
    this.pepperoni = pepperoni;
    this.mushrooms = mushrooms;
  }

  toBuilder() {
    const builder = new PizzaBuilder(this.size);
    if (this.cheese) builder.addCheese();
    if (this.pepperoni) builder.addPepperoni();
    if (this.mushrooms) builder.addMushrooms();
    return builder;
  }

  toString() {
    const toppings = [
      this.cheese && "cheese",
      this.pepperoni && "pepperoni",
      this.mushrooms && "mushrooms",
    ].filter(Boolean);
    return `Pizza(${this.size}, ${toppings.join(", ") || "plain"})`;
  }
}

class PizzaBuilder {
  constructor(size) {
    this.size = size;
    this.cheese = false;
    this.pepperoni = false;
    this.mushrooms = false;
  }

  addCheese() { this.cheese = true; return this; }
  addPepperoni() { this.pepperoni = true; return this; }
  addMushrooms() { this.mushrooms = true; return this; }
  build() { return new Pizza(this.size, this.cheese, this.pepperoni, this.mushrooms); }
}

// Usage
const pizza = new PizzaBuilder("large").addCheese().addPepperoni().build();
console.log(pizza.toString()); // Pizza(large, cheese, pepperoni)

// Copy method: modify an existing pizza without rewriting its config
const modifiedPizza = pizza.toBuilder().addMushrooms().build();
console.log(modifiedPizza.toString()); // Pizza(large, cheese, pepperoni, mushrooms)
